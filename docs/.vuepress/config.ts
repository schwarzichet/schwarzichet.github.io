import { defineUserConfig } from 'vuepress'
import type { DefaultThemeOptions } from 'vuepress'
import fs from 'fs';
import glob from 'glob';
const parseMD = require('parse-md').default

const getDirContent = (source: fs.PathLike) =>
    fs.readdirSync(source, { withFileTypes: true })
        .filter(entry => entry.name[0] != '.' && entry.name != 'README.md').sort((a, b) => parseInt(b.name) - parseInt(a.name)).map(entry => source + entry.name)

const getMetaDataDate = (source: Date) =>
    new Date(parseMD(fs.readFileSync('docs' + source, 'utf8'))['metadata']['release_date'])


let allDir = glob.sync('docs/**/').map(f => '/' + f.substring(5));
var result = {}
allDir.forEach(i => {
    result[i] = [{
        text: i.split('/').slice(-2)[0],
        children: getDirContent('docs' + i).map(entryName => {
            if (!entryName.endsWith('.md')) {
                return entryName.substring(4) + '/'
            } else {
                return entryName.substring(4)
            }
        }),
        link: i
    }]
});

result['/'][0]['text'] = 'ZJU Console'
result['/game/'][0]['text'] = 'Game'
result['/anime/'][0]['text'] = 'Anime'

for (const [key, value] of Object.entries(result)) {
    const temp = key.split('/').filter(i => i != '');
    if (temp.length == 2 && /^\d+$/.test(temp[temp.length - 1])) {
        result[key][0]['children'].sort((a: any, b: any) => getMetaDataDate(b).getTime() - getMetaDataDate(a).getTime())
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
    description: 'a document for ZJU Console',
    bundler: '@vuepress/vite',

    // theme: path.resolve(__dirname, 'theme'),
    themeConfig: {
        contributors: false,
        logo: '/images/zju_console.jpg',
        sidebar: result,
        notFound: ['You Lost'],
        lastUpdated: false

    },

    plugins: [
        [
            '@vuepress/plugin-search',
            {
                maxSuggestions: 100,
            },

        ]
    ],

})
