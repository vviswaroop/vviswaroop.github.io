import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const blog = await getCollection('blog');
  return rss({
    title: 'Viswaroop Vadlamudi | Agentic AI & Platform Engineering',
    description: 'Deep dives on Agentic AI Infrastructure, Identity Boundaries, and Platform Engineering.',
    site: context.site || 'https://vviswaroop.github.io',
    items: blog.map((post) => ({
      title: post.data.title,
      pubDate: post.data.date,
      description: post.data.description || `Read ${post.data.title} by ${post.data.author}`,
      link: `/blog/${post.slug}/`,
    })),
    customData: `<language>en-us</language>`,
  });
}
