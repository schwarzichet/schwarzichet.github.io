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
        children: getDirContent('docs' + i).map(dirname => dirname.substr(4) + '/')
    }]
});


export default defineUserConfig<DefaultThemeOptions>({
    lang: 'en-US',
    title: 'ZJU Console',
    description: 'Just playing around',

    themeConfig: {
        // logo: 'https://vuejs.org/images/logo.png',
        sidebar: result,

    }
})
