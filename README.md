# Cobot Project
A Cobot is like a coworker, but it is entirely based on a language model. Check back soon for this project to be updated with working samples.  

# Update 3.6.25

🤖 Cloudfare "worker" [agents](https://github.com/cloudflare/agents) can now be deployed and combined with Google's new [Generative AI Toolbox](https://googleapis.github.io/genai-toolbox). The result is a worker that can access tools like SQL databases, email, calendar, and so on. The aims of this project will adhere to the human-in-the-loop process flow outlined in Cloudfare's documentation:

![Human-in-the-Loop](https://developers.cloudflare.com/_astro/human-in-the-loop.Bx0axRJl_Z1cWd5M.svg)

# Update 2.24.25

🧠 MemoryBot: Your AI Conversation Companion! 💬✨ This smart script creates a seamless chat experience with AI that actually remembers your conversations! 🤯 It saves your entire chat history 📚 while cleverly summarizing older parts to keep costs down 💰⬇️. With pretty-printed responses 🎨, automatic saving 💾, and intelligent memory management 🧩, you'll never lose an important conversation again! The dual-LLM system acts like your personal AI secretary 🤖👔 - one part chats while the other organizes memories! Perfect for students 🎓, developers 👩‍💻, researchers 🔬, or anyone who wants meaningful, continuous conversations with AI without breaking the bank! 💪🚀 [Check it out!](/samples/memory-bot.py)  

![SCreenshot of a Cobot](/media/Cobot.webp)

<details>  

<summary>⌛ Updates</summary>
  
## Index

2.24.25 - [memory-bot.py](/samples/memory-bot.py) is a recently released script that deploys a powerful memory capable agent to store conversations for later analysis. It also uses recursive recalling to build memory states from summaries of previous memory states (An inception of LLM agents, one summarizing and another interacting with the user).  

[STT_AI.ipynb](/samples/STT_AI.pynb) is a jupyter notebook that contains a working sample of the Speech to Text LLM summarization task. (Currently tested and working.)\
\
[Tinytroupe_analyzer.py](/samples/Tinytroupe_analyzer.py) is an exercise in using Microsoft's TinyTroupe to deploy agent brainstorming sessions. This is purely for educational purposes only.\
\
[Vision_AI.pynb](/samples/Vision_AI.pynb) is a jupyter notebook that contains a working sample of the Open AI Vision engine. (Currently tested and working.)\
\
Helium_AI.pynb *will* be a jupyter notebook that contains a working sample of Helium web navigation functions to run in tandem with the Open AI text generator engine.
(Currently in development.)

</details>
