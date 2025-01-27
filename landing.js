const canvas = document.getElementById("bgCanvas");
const mainCtx = canvas.getContext("2d");

const offscreenCanvas = document.createElement('canvas');
const offscreenCtx = offscreenCanvas.getContext('webgl');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const smallWidth = Math.min(512, canvas.width);
const smallHeight = Math.trunc(smallWidth * canvas.height/canvas.width);
offscreenCanvas.width = smallWidth;
offscreenCanvas.height = smallHeight;

const gl = offscreenCtx;

gl.viewport(0, 0, offscreenCanvas.width, offscreenCanvas.height);

const fragmentShaderSource = `
    precision mediump float;
    uniform float iTime;
    uniform vec2 iResolution;

    float hash(vec2 uv)
    {
        float r;
        uv = abs(mod(10.*fract((uv+1.1312)*31.),uv+2.));
        uv = abs(mod(uv.x*fract((uv+1.721711)*17.),uv));
        return r = fract(10.* (7.*uv.y + 31.*uv.x));
    }

    // CREDIT: https://www.shadertoy.com/view/XsXXDn
    vec3 bg1(){
        float t = iTime/5.0;
        vec2 r = iResolution.xy;
        vec3 c;
        float l,z=t;
        for(int i=0;i<3;i++) {
            vec2 uv,p=gl_FragCoord.xy/r;
            uv=p;
            p-=.5;
            p.x*=r.x/r.y;
            z+=.07;
            l=length(p);
            uv+=p/l*(sin(z)+1.)*abs(sin(l*9.-z-z));
            c[i]=.01/length(mod(uv,1.)-.5);
        }
        return min(vec3(2.0), c/l);
    }

    #define iterations 17
    #define formuparam 0.53

    #define volsteps 20
    #define stepsize 0.1

    #define zoom   0.800
    #define tile   0.850
    #define speed  0.010 

    #define brightness 0.0015
    #define darkmatter 0.300
    #define distfading 0.730
    #define saturation 0.850


    // CREDIT: https://www.shadertoy.com/view/XlfGRj
    vec3 bg2()
    {
        vec2 iMouse = vec2(0.0);

        //get coords and direction
        vec2 uv=gl_FragCoord.xy/iResolution.xy-.5;
        uv.y*=iResolution.y/iResolution.x;
        vec3 dir=vec3(uv*zoom,1.);
        float time=iTime*speed+.25;

        //mouse rotation
        float a1=.5+iMouse.x/iResolution.x*2.;
        float a2=.8+iMouse.y/iResolution.y*2.;
        mat2 rot1=mat2(cos(a1),sin(a1),-sin(a1),cos(a1));
        mat2 rot2=mat2(cos(a2),sin(a2),-sin(a2),cos(a2));
        dir.xz*=rot1;
        dir.xy*=rot2;
        vec3 from=vec3(1.,.5,0.5);
        from+=vec3(time*2.,time,-2.);
        from.xz*=rot1;
        from.xy*=rot2;
        
        //volumetric rendering
        float s=0.1,fade=1.;
        vec3 v=vec3(0.);
        for (int r=0; r<volsteps; r++) {
            vec3 p=from+s*dir*.5;
            p = abs(vec3(tile)-mod(p,vec3(tile*2.))); // tiling fold
            float pa,a=pa=0.;
            for (int i=0; i<iterations; i++) { 
                p=abs(p)/dot(p,p)-formuparam; // the magic formula
                a+=abs(length(p)-pa); // absolute sum of average change
                pa=length(p);
            }
            float dm=max(0.,darkmatter-a*a*.001); //dark matter
            a*=a*a; // add contrast
            if (r>6) fade*=1.-dm; // dark matter, don't render near
            //v+=vec3(dm,dm*.5,0.);
            v+=fade;
            v+=vec3(s,s*s,s*s*s*s)*a*brightness*fade; // coloring based on distance
            fade*=distfading; // distance fading
            s+=stepsize;
        }
        v=mix(vec3(length(v)),v,saturation); //color adjust
        return v*0.01; 
    }

    void main()
    {
        vec2 uv = (2.0*gl_FragCoord.xy-iResolution.xy)/iResolution.y;
        // vec2 uv = .5*(abs(sin(iTime/2.))+.5)*(2.0*gl_FragCoord.xy-iResolution.xy)/iResolution.y;
        float vignette = length(0.6*uv.xy);
        // vignette *= vignette;
        // vignette *= vignette;
        vignette = 0.1*max(1.0 - vignette, 0.);
        // uv.x = hash(vec2(hash(uv),1.0));
        float quant_scale = 10.0;
        vec2 uv_quant = floor(uv * quant_scale) / quant_scale;
        // float noise = hash(uv_quant+iTime);
        // float noise = hash(uv_quant+iTime/1000000.);
        float noise = hash(uv_quant+iTime/10000000.);

        // vec3 bg = bg1();
        vec3 bg = bg2();
        // vec3 bg = vec3(1.0);

        gl_FragColor = vec4(bg*vec3(noise)*vignette + 0.05, 1.);
    }

    // void main() {
    //     vec3 color = vec3(gl_FragCoord.xy/res, 0.4);
    //     gl_FragColor = vec4(color, 1.0);
    // }
`;

function createShader(type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error("ERROR compiling shader!", gl.getShaderInfoLog(shader));
    }
    return shader;
}

const vertexShaderSource = `
    attribute vec2 position;
    void main() {
        gl_Position = vec4(position, 0.0, 1.0);
    }
`;
const vertexShader = createShader(gl.VERTEX_SHADER, vertexShaderSource);
const fragmentShader = createShader(gl.FRAGMENT_SHADER, fragmentShaderSource);

const program = gl.createProgram();
gl.attachShader(program, vertexShader);
gl.attachShader(program, fragmentShader);
gl.linkProgram(program);
gl.useProgram(program);

const vertices = new Float32Array([
    -1.0, -1.0,
    1.0, -1.0,
    -1.0,  1.0,
    -1.0,  1.0,
    1.0, -1.0,
    1.0,  1.0,
]);

const positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

const positionLocation = gl.getAttribLocation(program, "position");
gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
gl.enableVertexAttribArray(positionLocation);

const timeLocation = gl.getUniformLocation(program, "iTime");
const resLocation = gl.getUniformLocation(program, "iResolution");

function render(time) {
    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.uniform1f(timeLocation, time * 0.001);
    gl.uniform2f(resLocation, offscreenCanvas.width, offscreenCanvas.height)
    gl.drawArrays(gl.TRIANGLES, 0, vertices.length / 2);

    mainCtx.imageSmoothingEnabled = false;
    mainCtx.clearRect(0, 0, canvas.width, canvas.height);
    mainCtx.drawImage(offscreenCanvas, 0, 0, canvas.width, canvas.height);
            
    requestAnimationFrame(render);
}

render(0);
