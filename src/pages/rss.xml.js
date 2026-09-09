import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const blog = (await getCollection('blog')).sort((a,b)=>b.data.date.valueOf()-a.data.date.valueOf());
  return rss({
    title: 'Viswaroop Vadlamudi — Systems & notes',
    description: 'Notes on platforms, identity, books, and learning along the way.',
    site: context.site || 'https://viswaroop.dev',
    items: blog.map((post) => ({
      title: post.data.title,
      pubDate: post.data.date,
      description: post.data.description || `Read ${post.data.title} by ${post.data.author}`,
      link: `/blog/${post.slug}/`,
    })),
    customData: `<language>en-us</language>`,
  });
}
