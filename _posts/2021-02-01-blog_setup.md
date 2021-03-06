---
layout: single
title:  "Setting up the blog"
date:   2021-02-01
---

Hello world!!

I thought I will start of by posting on how I setup this blog.
First I decided to use 
[GitHub Pages](https://pages.github.com/)
since I already had a Github account and it sounded simple to set it up.
Not simple at all as it turned out.
While there are many posts around with headlines like
setup your blog in 5 minutes, the reality is that 
it takes 5 minutes if you want to setup an exact replica of a pre-existing template.
Figure out how to do even the most simple customizations can take quite some time.
Let us begin then.

## First steps 

I decided to use Jekyll since that is what Github recommends.
Now, Jekyll requires Ruby. A version of Ruby is already available on Mac. 
However, I had some issues, so I used Homebrew to install Ruby.
If you don't have Ruby, please install it for your platform. 
Next, create a directory where you will keep the website files and 
in the terminal do the following inside this directory.

```
gem install bundler jekyll
```

Now, we could use the steps listed at various steps such as
[here](https://www.freecodecamp.org/news/create-a-free-static-site-with-github-pages-in-10-minutes/)
to use the default theme.
But I decided to use the 
[Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes)
theme which looked better.
Download the repository to your folder and then inside the folder do

```
bundle update
```

And you are done! You can view your website by doing 

```
bundle exec jekyll serve  
```

and then putting the following in your browser.

```
http://localhost:4000/
```

That took 5 minutes. So what's the problem.
Well, quite a few of them. But first, the easy part.
Use the `_config.yml` to change things such as the name of the website,
your social media links etc. 
Every time, you make a change, you can do the above steps to open it in the browser
and check the results.
Its exactly like compiling and running!

## Customize

The very first thing I wanted to do was figure out how to add
a page for blog posts.
To do this add a folder `_pages` in the home directory
and inside this directory add a file called `blog.md`.
Write the following inside this file

```
---
title:  "Blog"
layout: archive
permalink: /Blog/
author_profile: true
---

```

Next edit the file `_data/navigation.yml` to look like this.

```
main:
  - title: "Blog"
    url: /Blog/
```

This completes the setup. To write posts, create a new folder
`_posts` and add blog posts there. The file must be named like this.

```
yyyy-mm-dd-name.md
```

The top of the file must have

```
---
layout: single
title:  "Name"
date:   yyyy-mm-dd
---
```

and then start writing your post below. Note that if you name the files with `.md` 
extension, you are basically telling Jekyll that you are using 
[Markdown](https://guides.github.com/features/mastering-markdown/).
So we are done with setting up blogging.
There's a slight hitch though, although this is just a personal choice.
With this setup Jekyll puts the posts on your home page. 
I did not want this.
So I deleted the `index.html` page in the home directory
and added an `index.md` file with the following lines.

```
---
title: 'About me'
layout: single
author_profile: true
---
```

One more customization I decided to do was to add a newsletter sign-up form.
To do this, I signed up at 
[Mailchimp](https://mailchimp.com/)
and created an embedded signup form. 
Mailchimp gave me the HTML for the form which I copy-pasted into a new file
`_data/signup.html`.
I also added the following line into `_layouts/single.html`.

```
{# if page.signup == true #}{# include signup.html #}{# endif #}.
```
Replace `#` with `%` in the above. Jekyll thinks I am trying to execute
this from inside the blog post.
I modified the defaults in `_config.yml` to add the signup line.  

```
defaults:
  - scope:
      path: ""
      type: posts
    values:
      layout: single
      author_profile: true
      share: true
      related: true
      signup: true
      signup: true
```

Finally, in `_pages/blog.md` I added the following in the header.

```
signup: true
```

Phew!!
And now we need to do the easiest part. 
Put it all online. 
Go to your GitHub account, and setup a new repository `username.github.io`.
From the terminal do

```
git init
git remote add origin git@github.com:<your_github_username>/<your_github_repo_name>.git
git add *
git commit -m "Setting up Jekyll"
git push -u origin master
```

And we are done.
So that is how I setup my blog. 
Of course I continue to change things here and there. 
If you are interested, have a look at the files on my GitHub.

<br />


