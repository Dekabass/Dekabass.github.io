'''
--- Some docs ---

Landing - ./index.html
Pages - ./<name>
404 - 404.html

Artist data - data/artists.json
Release data - data/releases.json

Expected artist keys - 
    name
    type (core|satellite|past)
    links
        (social media name): url
        ...
    img
    oneliner
    bio

Expected release keys - 
    name
    date (M D Y)
    date_end (optional "M D Y" or "ongoing")
    img
    tracks
        name (optional)
        artists (list)
    links (if >1 tracks)
        (social media name): url
'''

# -------- UTIL -------- #

import json
from html import *
from datetime import datetime

# load artists
with open('data/artists.json', 'r') as f:
    artists = json.load(f)
def get_sorted_artists(artist_type):
    return sorted([a for a in artists if a['type'] == artist_type], key=(lambda x: x['name'].lower()))

# load releases
with open('data/releases.json', 'r') as f:
    releases = json.load(f)
DATE_FMT = "%b %d %Y"
for r in releases:
    r['date'] = datetime.strptime(r['date'], DATE_FMT)
    if 'date_end' in r and r['date_end'] != 'ongoing':
        r['date_end'] = datetime.strptime(r['date_end'], DATE_FMT)
releases = sorted(releases, key=(lambda x: x['date']), reverse=True)
releases_by_yr = {}
for r in releases:
    yr = r['date'].year
    if yr not in releases_by_yr:
        releases_by_yr[yr] = []
    releases_by_yr[yr].append(r)

def unfmt(s):
    return s.lower().replace(' ', '')

chroma_filter = '''
<svg width="0" height="0">
    <filter id="chroma">
        <feColorMatrix type="matrix" 
        result="red_"             
        values="4 0 0 0 0
                0 0 0 0 0 
                0 0 0 0 0 
                0 0 0 1 0"/>
        <feOffset in="red_" dx="2" dy="0" result="red"/>
        <feColorMatrix type="matrix" 
        in="SourceGraphic"             
        result="blue_"             
        values="0 0 0 0 0
                0 3 0 0 0 
                0 0 10 0 0 
                0 0 0 1 0"/>
        <feOffset in="blue_" dx="-3" dy="0" result="blue"/>    
        <feBlend mode="screen" in="red" in2="blue"/>
    </filter>
</svg>
'''

def make_page(name, content, page_title=None, extra_head=None):
    with open(f'./{unfmt(name)}.html', 'w') as f:
        f.write(html(
            head(
                meta(charset='UTF-8'),
                meta(name='viewport', content='width=device-width, initial-scale=1.0'),
                meta(name='keywords', content='Dekabass'),
                meta(name='description', content='The home of Dekabass, a collective of musicians making music.'),
                link(rel='icon', href='https://raw.githubusercontent.com/Dekabass/Dekabass.github.io/master/img/dekalogo-transparent.png', type='img/png'),
                meta(name='og:image', content='https://raw.githubusercontent.com/Dekabass/Dekabass.github.io/master/img/dekalogo-transparent.png'),
                title(page_title or (name + ' - Dekabass')),
                link(href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap', rel='stylesheet'),
                link(rel='stylesheet', href='styles.css'),
                extra_head or ''
            ),
            body(
                content,
                chroma_filter
            ),
            lang="en"
        ))

def make_header(current_page_name):
    headers = [
        ('Home', '/'),
        ('Artists', None),
        ('Releases', None),
        ('Contact', None),
        ('About Us', None)
    ]
    bg = f'background-color: var(--{unfmt(current_page_name)}-col);'
    return header(
        div(),
        img(src='img/dekalogo-transparent.png', alt='Dekabass Logo', class_='logo'),
        div(
            elems(
                a(
                    name,
                    href=(place or unfmt(name)),
                    style=(bg if name==current_page_name else '')
                )
                for name, place in headers
            ),
            class_='nav-buttons nav-buttons-scheme2'
        ),
        div(),
    )

def make_artist_social_media(link_data):
    return div(
        elems(
            a(
                img(src=f'img/sm-{k}.png', alt=k),
                href=v, target='_blank'
            )
            for k,v in link_data.items()
        ),
        class_='artist-social-media social-media'
    )

def make_social_media_section():
    return section(
        div(
            a(
                img(src='img/sm-youtube.png', alt='youtube'),
                href='https://www.youtube.com/channel/UCzRcRpI8z3Cv-wFFMbEecwg', target='_blank'
            ),
            a(
                img(src='img/sm-soundcloud.png', alt='soundcloud'),
                href='https://soundcloud.com/dekabass', target='_blank'
            ),
            a(
                img(src='img/sm-discord.png', alt='discord'),
                href='https://discord.gg/HKCd944Ct6', target='_blank'
            ),
            a(
                img(src='img/sm-newgrounds.png', alt='discord'),
                href='https://dekabass.newgrounds.com', target='_blank'
            ),
            br(),
            img(src='img/dekasignature.png', class_='sig'),
            class_='social-media landing-social-media'
        ),
    )

# -------- 404 -------- #

make_page('404',
    content=elems(
        h1('404'),
        p('It seems you have gotten lost in the kingdom.'),
        a(p('Where did I come in, again?'), href='./index.html')
    ),
)

# -------- About -------- #

make_page('About Us',
    elems(
        main(
            make_header('About Us'),
            section(
                div(
                    div(),
                    h2('Who Are We?'),
                    div(),
                    class_='section-title'
                ),
                p('We are a collective of musicians making music in a centuries old kingdom. Our kingdom is ruled by the council of core members along with their indispensable satellites. You can see all members of the ruling class ', a('here', href='artists'), '.', class_='center-p'),
            ),
            section(
                div(
                    div(),
                    h2('<i>Why</i> Are We?'),
                    div(),
                    class_='section-title'
                ),
                p('Our kingdom was birthed from the picturesque rolling hills overlaying the kingdom of Xtrullor. In this kingdom (er, Discord server), the core members convened for the first time with the shared purpose of sonic creation. They were determined to forge a single musical track where all of them serve as participants in its creation - a megacollab. But alas, this undertaking isn\'t possible by any mere mortals. Despite the setback, the hopes and dreams of our heros remained unscathed. Instead, they spent the next few centuries starting a brand new kingdom - the kingdom of Dekabass. Ever since then, the ruling class of this new kingdom has been unendingly determined to create the best bass music possible, all the while building a community around that music.', class_='center-p'),
            ),
            section(
                div(
                    div(),
                    h2('When Do Our Next Releases Come Out?'),
                    div(),
                    class_='section-title'
                ),
                p('We don\'t have an exact release schedule per se. But, there <i>are</i> still some regular releases..? it\'s complicated. You can read about it in ', a('releases', href='releases'), '.', class_='center-p'),
            ),
            section(
                div(
                    div(),
                    h2('Can I Be a Satellite Member?'),
                    div(),
                    class_='section-title'
                ),
                p('Sure! ', a('Contact us', href='contact'), ' to apply.', class_='center-p center-text'),
            ),
            section(
                div(
                    div(),
                    h2('Can I Be a Core Member?'),
                    div(),
                    class_='section-title'
                ),
                p('No.', class_='center-p center-text')
            ),
            section(
                div(
                    div(),
                    h2('Who Made This Website?'),
                    div(),
                    class_='section-title'
                ),
                p('It was made by', a('not_woowoo', href='artists#artist-not_woowoo'), ';) with the help of core members and satellite members.', class_='center-p'),
            ),
            section(
                div(
                    div(),
                    h2('The Ancient Tale of Dekabass'),
                    div(),
                    class_='section-title'
                ),
                p('''
There was once a quaint kingdom that lay on the hills between Au5ia and Shponggleland: the Kingdom of Xtrullor.
It was an ordinary night in the kingdom. Locals stood at the center of anarchy in the streets while the king sat upon his majestic purple throne - busy with what the scholars called "real life."
That night, a local bard found himself partaking in the art of conversation with some other local bards. Despite not having known each other before, the countless bards got along well. An outsider looking in could assume that they had known each other for ages before that fateful night.
From the passing sparks of conversation, an idea hatched from within the narrows of one bard's mind. That bard took one look around the room, and released his idea into the open, "Yo, what if we did xtrulor server megacollab?!"
Like a beacon of light illuminating a world submerged in eternal darkness, those simple words attracted attention and blossomed into intrigue from not only the bards, but also the peasants and even the pagans.
A scramble of ideas from the collective minds of the kingdom ensued; the citizens started to form something new from the rubble of anarchy. Once the dust and debris of chaotic planning had settled, god rays shined as the sun peaked over the horizon, and the sun's warm light fell on 10 bards from the kingdom as if destiny itself hand picked the 10 bards to start something new. ​
A brand new kingdom was settled downhill from the old Kingdom of Xtrullor, and it was founded under the field of thought known as "Megacollab," where all the citizens of the kingdom would work towards one common goal of making an epic tune. A name was eventually decided for the new kingdom that honored its origins: Dekabass. "Deka" meaning 10 for the original 10 bards that settled the new land, and "bass" referring to the ancient art of "bass" in music.
When the first houses and the town hall were erected on the fertile ground of the new lands, king Xtrullor of lands that were back so far up the hill mysteriously made himself present in the new lands, and he still remains to this day for reasons unknown.
Progress of the new kingdom started as a burst, but soon dwindled as supplies inevitably ran low. Apathy and malaise now plagued the new land's governing powers, and major reforms were put in place - 
now, this kingdom no longer worked towards a single "Megacollab," but instead operated under the goal of establishing many new tunes from different bards around the world, but mostly the 10 that founded it - otherwise known as a "collective," or a "label."
Ever since the early days of the kingdom, much has changed: the number of governing bards has changed, the old king Xtrullor renounced his position in government (but still remained in a village), and even the original "Megacollab" has since disintegrated into ashes of what it once was. But, the kingdom still serves as a means of creation; the creation of epic music.
The future of Dekabass is a blur from where we stand in the present, but it isn't hard to see how bright it is. 
'''.strip(), class_='center-p'),
            ),
            make_social_media_section()
        )
    )
)

# -------- Contact -------- #

make_page('Contact',
    elems(
        main(
            make_header('Contact'),
            section(
                div(
                    div(),
                    h2('How Can I Contact Dekabass?'),
                    div(),
                    class_='section-title'
                ),
                p('Contact us via messenger pigeon.', class_='center-p'),
                br(),
                p('If that doesn\'t work for you, then feel free to let yourself into our ', a('Discord server', href='https://discord.gg/HKCd944Ct6'), '. Discord is our preferred method of communication when it comes to: <b>applications</b>, commenting on music, asking questions, label/collective relations, and copyright issues. You can also email us here:', class_='center-p'),
                br(),
                p('DekabassMusic@gmail.com', class_='center-p center-text'),
            ),
            section(
                div(
                    div(),
                    h2('How Can I Apply to Join?'),
                    div(),
                    class_='section-title'
                ),
                p('Our Discord server has an #applications channel. See the pinned messages in #applications for further instruction on applying to become a satellite.', class_='center-p'),
            ),
            make_social_media_section()
        )
    )
)

# -------- Releases -------- #

def make_track_artists(data):
    artists_w_links = [
        a(name, href='artists#artist-'+unfmt(name), style="font-weight:bold; color: #fff;")
        for name in data
    ]
    return div(', '.join(artists_w_links))

def make_release_tracks(data):
    return elems(
        div(
            make_track_artists(track['artists']),
            div(track['name'], class_='track-name'),
            class_='comp-tracks'
        )
        for track in data
    )

def make_release_card(data):
    is_single = len(data['tracks']) == 1
    date_str = data['date'].strftime("%B %-d")
    if 'date_end' in data:
        date_str += ' - '
        if data['date_end'] == 'ongoing':
            date_str += span('ONGOING', style='color:var(--releases-col);')
        else:
            date_str += data['date_end'].strftime("%B %-d") 
    info = (
        make_track_artists(data['tracks'][0]['artists']) if is_single else
        make_release_tracks(data['tracks'])
    )
    return div(
        img(src=data['img'], class_='track-img'),
        div(
            div(data['name'], class_='artist-name'),
            div(date_str, class_='artist-oneliner'),
            div(info, class_='rel-info'),
            make_artist_social_media(data['links']),
            class_='artist-info'
        ),
        class_='artist-card'
    )

make_page('Releases',
    elems(
        main(
            make_header('Releases'),
            section(
                div(
                    div(),
                    h2('What are "Releases?"'),
                    div(),
                    class_='section-title'
                ),
                p('<b>Releases are the musical output of core members and satellite members.</b> All releases are listed below chronologically. Each release is a collection of one or more tracks where each track created by one or more artists.', class_='center-p'),
                br(),
                p('As for a release schedule, we regularly release an <i>anniversary</i> album every January. Other than that, all releases are done intermitantly without a regular schedule.', class_='center-p')
            ),
            elems(
                section(
                    div(
                        div(),
                        h2(f'{yr}'),
                        div(),
                        class_='section-title'
                    ),
                    div(
                        elems(make_release_card(r) for r in rs),
                        class_='artists-container'
                    )
                ) for yr, rs in releases_by_yr.items()
            ),
            make_social_media_section()
        )
    )
)

# -------- Artists -------- #

def make_artist_card(data):
    return div(
        img(src=data['img'], class_='artist-img'),
        div(
            div(data['name'], class_='artist-name', id='artist-'+unfmt(data['name'])),
            div(data['oneliner'], class_='artist-oneliner'),
            div(data['bio'], class_='artist-bio'),
            make_artist_social_media(data['links']),
            class_='artist-info'
        ),
        class_='artist-card'
    )

make_page('Artists',
    elems(
        script('''
// Scroll to target element
function centerTarget() {
const target = document.querySelector(location.hash);
    if (target) {
      const targetRect = target.getBoundingClientRect();
      const scrollY = window.scrollY || window.pageYOffset;
      
      const centerPosition = targetRect.top + scrollY - (window.innerHeight / 2) + (targetRect.height / 2);
      
      window.scrollTo({
        top: centerPosition,
        behavior: 'smooth'
      });
    }
}

window.addEventListener('load', () => {
    if(location.hash)
        centerTarget();
});
'''),
        main(
            make_header('Artists'),
            section(
                div(
                    div(),
                    h2('Who is an "Artist?"'),
                    div(),
                    class_='section-title'
                ),
                p(b('Anyone who has or is planned to release music on Dekabass'), 'is an artist. Artists are in one of 3 categories: core members, satellite members, and past members. You can read more on types of artists ', a('here.', href='#artist-categories'), 'All artists are listed alphabetically.', class_='center-p'),
            ),
            section(
                div(
                    div(),
                    h2('Core Members'),
                    div(),
                    class_='section-title'
                ),
                div(
                    elems(
                        make_artist_card(artist)
                        for artist in get_sorted_artists('core')
                    ),
                    class_='artists-container'
                )
            ),
            section(
                div(
                    div(),
                    h2('Satellite Members'),
                    div(),
                    class_='section-title'
                ),
                div(
                    elems(
                        make_artist_card(artist)
                        for artist in get_sorted_artists('satellite')
                    ),
                    class_='artists-container'
                )
            ),
            section(
                div(
                    div(),
                    h2('Past Members'),
                    div(),
                    class_='section-title'
                ),
                div(
                    elems(
                        div(
                            h3(artist['name'], id='artist-'+unfmt(artist['name'])),
                            make_artist_social_media(artist['links'])
                        )
                        for artist in get_sorted_artists('past')
                    ),
                    class_='past-artists-container'
                )
            ),
            section(
                div(
                    div(),
                    h2('Artist Categories'),
                    div(),
                    class_='section-title'
                ),
                p('Artists listed here are in one of three categories:'),
                div(
                    div(
                        h3('Core Members'),
                        p('These guys are hardcore. They are the ones who first settled the lands that became the kingdom of Dekabass. They regularly release music and won\'t be leaving any time soon. Some may say they "run" Dekabass.')
                    ),
                    div(
                        h3('Satellite Members'),
                        p('These people are far out. They are the highest class civilian denizens of the kingdom. We cannot guarantee that they\'ll release as regularly as core members (although many of them do). They aren\'t permanent members of Dekabass, but we hope to see them stick around.', a('Contact us', href='contact'), 'if you want to be a satellite member!')
                    ),
                    div(
                        h3('Past Members'),
                        p('There are some who no longer release music or haven\'t yet released music with us (despite wanting to', i('and'), 'being allowed into the kingdom). It\'s unlikely that our kingdom will once again be graced by the sonic experiences of these individuals, but that doesn\'t mean we can\'t list them here.')
                    ),
                    id='artist-categories'
                )
            ),
            make_social_media_section()
        )
    )
)

# -------- LANDING -------- #

make_page('index', page_title='Dekabass',
    extra_head=style('''
        /* Do not play animations until page is visible */
        .js-loading *,
        .js-loading *:before,
        .js-loading *:after {
            animation-play-state: paused !important;
        }
    '''),
    content=elems(
        script('''
            // Do not play animations until page is visible
            document.body.classList.add('js-loading');
            window.addEventListener("load", function(){
                if(!document.hidden){
                    document.body.classList.remove('js-loading');
                }
            });
            document.addEventListener('visibilitychange', function(e) {
                document.body.classList.remove('js-loading');
            });
        '''),

        canvas(id='bgCanvas'),

        img(src='img/dekalogo-transparent.png', alt='Logo', id='landing-logo'),
        
        h1('Dekabass', id='landing-title'),

        hr(class_='title-hr'),

        div(
            a('Artists', href='artists'),
            a('Releases', href='releases'),
            a('Contact', href='contact'),
            a('About Us', href='aboutus'),
            class_='nav-buttons landing-nav-buttons nav-buttons-scheme1'
        ),

        div(
            a(
                img(src='img/sm-youtube.png', alt='youtube'),
                href='https://www.youtube.com/channel/UCzRcRpI8z3Cv-wFFMbEecwg', target='_blank'
            ),
            a(
                img(src='img/sm-soundcloud.png', alt='soundcloud'),
                href='https://soundcloud.com/dekabass', target='_blank'
            ),
            a(
                img(src='img/sm-discord.png', alt='discord'),
                href='https://discord.gg/HKCd944Ct6', target='_blank'
            ),
            a(
                img(src='img/sm-newgrounds.png', alt='discord'),
                href='https://dekabass.newgrounds.com', target='_blank'
            ),
            class_='social-media landing-social-media'
        ),

        footer('&copy; 2025 Dekabass'),

        script(src='landing.js')
    )
)

print('Built Site')

