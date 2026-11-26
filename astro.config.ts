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
  redirects: {
    "/visuals": "/fcd/verhaal-presentatie/",
    "/showcases/showkitchen-mvp0": "/fcd/showcases/demo/",
    "/showcases/fcd-mvp0": "/fcd/showcases/demo/",
    "/en/visuals": "/fcd/en/verhaal-presentatie/",
    "/en/showcases/showkitchen-mvp0": "/fcd/en/showcases/demo/",
    "/en/showcases/fcd-mvp0": "/fcd/en/showcases/demo/",
    "/showcases/in-werking": "/fcd/showcases/demo/",
    "/en/showcases/in-werking": "/fcd/en/showcases/demo/",
  },
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
        {
          label: "Het verhaal",
          slug: "verhaal-presentatie",
          translations: { en: "The story" },
        },
        {
          label: "Het FCD-model",
          translations: { en: "The FCD model" },
          items: [
            { label: "Het FCD-model", slug: "model", translations: { en: "The FCD model" } },
            { label: "Terminologie", slug: "terminologie", translations: { en: "Terminology" } },
          ],
        },
        { label: "Jouw FCD-model", slug: "jouw-fcd-model", translations: { en: "Your FCD model" } },
        {
          label: "Showcases",
          items: [
            { label: "Overzicht", slug: "showcases", translations: { en: "Overview" } },
            {
              label: "Demo",
              items: [
                { label: "Demo", slug: "showcases/demo" },
                { label: "The making of", slug: "showcases/demo/making-of" },
              ],
            },
            { label: "Classic", slug: "showcases/classic" },
            { label: "Ideal", slug: "showcases/ideal" },
          ],
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
