import { defineUserConfig } from 'vuepress'
import type { DefaultThemeOptions } from 'vuepress'
import fs from 'fs';
import glob from 'glob';
import path from 'path'
const parseMD = require('parse-md').default

const getDirContent = (source: fs.PathLike) =>
    fs.readdirSync(source, { withFileTypes: true })
        .filter(entry => entry.name[0] != '.' && entry.name != 'README.md').sort((a, b) => parseInt(b.name) - parseInt(a.name)).map(entry => source + entry.name)

const getMetaDataDate = (source) =>
        new Date(parseMD(fs.readFileSync('docs'+source, 'utf8'))['metadata']['game_release_date'])


let allDir = glob.sync('docs/**/').map(f => '/' + f.substr(5));
var result = {}
allDir.forEach(i => {
    result[i] = [{
        isGroup: true,
        text: i.split('/').slice(-2)[0],
        children: getDirContent('docs' + i).map(entryName => {
            if (!entryName.endsWith('.md')) {
                return entryName.substr(4) + '/'
            } else {
                return entryName.substr(4)
            }
        }),
        link: i
    }]
});

result['/'][0]['text'] = 'ZJU Console'
result['/game/'][0]['text'] = 'Game'

for (const [key, value] of Object.entries(result)) {
    const temp = key.split('/').filter(i => i != '');
    if (temp.length == 2 && /^\d+$/.test(temp[temp.length - 1])) {
        // console.log(result[key])
        result[key][0]['children'].sort((a: any, b: any) => getMetaDataDate(b) - getMetaDataDate(a))
        result[key].unshift(
            {
                text: "Back",
                link: '/' + temp[0] + '/'
            })
    }
}

export default defineUserConfig<DefaultThemeOptions>({
    lang: 'en-US',
    title: 'ZJU Console',
    description: 'Just playing around',
    bundler: '@vuepress/vite',

    // theme: path.resolve(__dirname, 'theme'),
    themeConfig: {
        contributors: false,
        logo: '/images/zju_console.jpg',
        sidebar: result,

    },

    plugins: [
        [
            '@vuepress/plugin-search',
            {
                maxSuggestions: 100,
            },
        ],
    ],
})
