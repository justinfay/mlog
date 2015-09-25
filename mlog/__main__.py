from mlog import Blog, Renderer


if __name__ == "__main__":
    blog = Blog()
    blog.load_posts()
    renderer = Renderer(blog)
    renderer.render_to_files()
