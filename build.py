from mlog import Blog, BlogRenderer, config


if __name__ == "__main__":
    blog = Blog()
    blog.load_posts()
    renderer = BlogRenderer(blog)
    renderer.render_to_files()
