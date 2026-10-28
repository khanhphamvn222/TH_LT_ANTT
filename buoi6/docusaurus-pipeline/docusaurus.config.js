// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'DevSecOps Knowledge Base',
  tagline: 'CI/CD Pipeline Security & Automation',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://khanhphamvn222.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/pipeline-tutorial/',

  // GitHub pages deployment config.
  organizationName: 'khanhphamvn222',
  projectName: 'pipeline-tutorial',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'vi',
    locales: ['vi'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'DevSecOps Lab 6',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Tài liệu thực hành',
          },
          {
            href: 'https://github.com/khanhphamvn222/TH_LT_ANTT',
            label: 'GitHub Repository',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        copyright: `Copyright © ${new Date().getFullYear()} Phạm Duy Khánh (MSSV: 2387700029) - TH_LT_ANTT.`,
      },
    }),
};

module.exports = config;
