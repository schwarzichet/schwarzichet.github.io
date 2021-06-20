import { defineUserConfig } from 'vuepress'
import type { DefaultThemeOptions } from 'vuepress'
import fs from 'fs';
import glob from 'glob';

const getDirContent = (source: fs.PathLike) =>
    fs.readdirSync(source, { withFileTypes: true })
        .filter(entry => entry.name[0] != '.' && entry.name != 'README.md')
        .map(entry => source + entry.name)


let allDir = glob.sync('docs/**/').map(f => '/' + f.substr(5));
var result = {}
allDir.forEach(i => {
    result[i] = [{
        isGroup: true,
        text: i.split('/').slice(-2)[0],
        children: getDirContent('docs' + i).map(dirname => dirname.substr(4) + '/'),
        link: i
    }]
});

result['/'][0]['text'] = 'ZJU Console'
result['/game/'][0]['text'] = 'Game'

for (const [key, value] of Object.entries(result)) {
    const temp = key.split('/').filter(i => i != '');
    if (temp.length == 2 && /^\d+$/.test(temp[temp.length - 1])) {
        result[key].unshift(
            {
                text: "Back",
                link: '/' + temp[0] + '/'
            })
    }
}


result['/game/2021/'].unshift({ text: "Back to Game", link: '/game/' })


export default defineUserConfig<DefaultThemeOptions>({
    lang: 'en-US',
    title: 'ZJU Console',
    description: 'Just playing around',
    bundler: '@vuepress/vite',

    themeConfig: {
        contributors: false,
        logo: '/images/zju_console.jpg',
        sidebar: result,

    },

    plugins: [
        [
            '@vuepress/plugin-search',
            {
                locales: {
                    '/': {
                        placeholder: 'Search',
                        maxSuggestions: 3,
                    }
                },
            },
        ],
    ],
})
