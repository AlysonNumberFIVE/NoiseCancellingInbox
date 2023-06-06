<<<<<<< Updated upstream
# NoiseCancellingInbox
Summarize away your subscriptions and noisy emails into a helpful, witty, weekly newsletter.

### The Only Newsletter you'll ever really need
Are you tired of thousands of emails every week? Is your inbox super noisy? Well golly gee willickers, do I have the solution for you!
Introducing noise cancelling headphones, **BUT FOR YOU INBOX**!

Now, you never have to waste countless hours reading through endless emails, notifications, receipts, blogs and anything elese you're interested in knowing about.

## How it Works

As you're peeking through this repo, you're probably tech savvy and wanna build it yourself. The basic ghist of it is that, using the **GMAIL API**, it pulls all your emails for the most recent week, and using **GPT-4**, it summarizes the content.

I did originally throw in some **Stability AI's** to generate those--you know how blogs have, like, images and thumbnails and stuff? To make them all quirk-looking, probably? Yeah, I wanted Stability to do that but it kept crashing... and when it didn't... well... you see...

Yeah...

## What you'll need

I'll start off by congratulating you for taking on the task of running this bad boi becuase it's waaaaaayy more work than I gave it credit for. I'll also throw a disclaimer here.

### It can get expensive if you're not careful with the prompt stuff

When it comes to GPT-4 costs, OpenAI's what I had under the hood. I'm starting the migration process with Vicura but I have a Macbook which doesn't have access to a GPU so my hands are somewhat tied. But it's a technical challegne I do wanna verse myself in. In the meantime, you'll have
to have access to both an **OpenAI API key as well as access to the GPT-4 model**. The GPT-4 part is almost a non-negotiable. GPT-3.5 is more affordable but isn't good at understanding and executing consistently on the prompts its givven.

### Stability AI API (Optional)

You can do what I initially was aiming to by adding auto-generated imagery to each of your summary's "headlines". I personally find its not worth it.
You're spending money on both GPT-4 to get it to give you an appropriate prompt for image generation based on the summarised info, and then sending it off to Stability AI for each of your stories.
Costs can get out of hand pretty quickly if you aren't careful.

### Gmail API

This is easily the most irritating of all the keys to just get to work. Not only that, but even after you get your keys, you then have to set up a small webserver that'll act as the proxy for where the emails are coming from.
I'm pretty sure most of that tech babble was correct. Jokes aside, if you haven't used Google's API stuff in a long time, accessing an inbox is considered **sensitive information access**. The rules have made inbox access a lot more secure
and the apps accessing your inbox have to have much higher security compliance than they used to (about 2 or so years ago). That's good news but has also increased the complexity of handling Gmail's API.

