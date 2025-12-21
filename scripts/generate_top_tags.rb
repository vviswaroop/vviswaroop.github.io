#!/usr/bin/env ruby
# scripts/generate_top_tags.rb
# Generates _data/top_tags.yml with top 6 tags by post count.
require 'yaml'
require 'fileutils'

posts = Dir['_posts/*.*'].map do |f|
  content = File.read(f)
  # Try YAML front matter parsing naive: extract between ---
  fm = content[/\A---\s*(.*?)\s*---/m, 1]
  next [] unless fm
  tags = []
  if fm =~ /tags:\s*\[([^\]]+)\]/m
    tags = $1.split(',').map { |t| t.strip.gsub(/['"]/, '') }
  else
    fm.scan(/^\s*-\s*(.+)$/).each do |m|
      tags << m.first.strip
    end if fm =~ /^tags:\s*$/m
  end
  tags
end.flatten.compact

counts = Hash.new(0)
posts.each { |t| counts[t] += 1 }

top = counts.sort_by { |_, c| -c }.first(6).map { |name, count| { 'name' => name, 'count' => count } }

FileUtils.mkdir_p('_data')
File.write('_data/top_tags.yml', top.to_yaml)
puts "Generated _data/top_tags.yml with #{top.length} tags"
