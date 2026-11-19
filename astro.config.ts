import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { unified } from "@astrojs/markdown-remark";
import { remarkSchuiven } from "./src/plugins/schuiven";
import { remarkLinks } from "./src/plugins/links";
import { remarkMermaid } from "./src/plugins/mermaid";

const base = "/fcd";

export default defineConfig({
  site: "https://fcd-labs.github.io",
  base,
  markdown: {
    processor: unified({
      remarkPlugins: [remarkSchuiven, remarkMermaid, [remarkLinks, { base }]],
    }),
  },
  integrations: [
    starlight({
      title: {
        nl: "Full Circle Delivery",
        en: "Full Circle Delivery",
      },
      description:
        "AI needs delivery. Delivery needs AI. Full Circle Delivery: het FCD-model, jouw FCD-model in een declaratief bestand, en een werkende showcase.",
      defaultLocale: "root",
      locales: {
        root: { label: "Nederlands", lang: "nl" },
        en: { label: "English", lang: "en" },
      },
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/fcd-labs/fcd",
        },
      ],
      editLink: {
        baseUrl: "https://github.com/fcd-labs/fcd/edit/main/",
      },
      customCss: ["./src/styles/custom.css"],
      components: {
        Footer: "./src/components/Footer.astro",
      },
      sidebar: [
        { label: "Home", slug: "index", translations: { en: "Home" } },
        { label: "Het FCD-model", slug: "model", translations: { en: "The FCD model" } },
        {
          label: "Showcases",
          items: [
            { label: "Overzicht", slug: "showcases", translations: { en: "Overview" } },
            { label: "ShowKitchen-MVP0", slug: "showcases/showkitchen-mvp0" },
            { label: "FCD-MVP0", slug: "showcases/fcd-mvp0" },
          ],
        },
        {
          label: "Verhaal en presentatie",
          slug: "verhaal-presentatie",
          translations: { en: "Story and presentation" },
        },
        {
          label: "Praatplaat en platen",
          slug: "visuals",
          translations: { en: "Talking picture and pictures" },
        },
        {
          label: "Terminologie",
          slug: "terminologie",
          translations: { en: "Terminology" },
        },
        { label: "Backlog", slug: "backlog" },
        {
          label: "Eerder werk",
          translations: { en: "Earlier work" },
          collapsed: true,
          items: [
            { label: "Overzicht", slug: "eerder-werk", translations: { en: "Overview" } },
            {
              label: "Scenario's",
              translations: { en: "Scenarios" },
              collapsed: true,
              items: [
                { label: "Overzicht", slug: "scenarios", translations: { en: "Overview" } },
                {
                  label: "Subdomein binnen enterprise",
                  slug: "scenarios/subdomein-enterprise",
                  translations: { en: "Subdomain within an enterprise" },
                },
                {
                  label: "Ontwerp subdomein",
                  slug: "scenarios/subdomein-enterprise-ontwerp",
                  translations: { en: "Design subdomain" },
                },
                { label: "Startup", slug: "scenarios/startup" },
              ],
            },
            {
              label: "Showcase practice",
              collapsed: true,
              items: [
                {
                  label: "Overzicht",
                  slug: "showcase-practice",
                  translations: { en: "Overview" },
                },
                {
                  label: "Contract-based testing",
                  slug: "showcase-practice/contract-based-testing",
                },
              ],
            },
            {
              label: "Open punten",
              slug: "open-punten",
              translations: { en: "Open items" },
            },
          ],
        },
        { label: "Over mij", slug: "over", translations: { en: "About me" } },
      ],
    }),
  ],
});
