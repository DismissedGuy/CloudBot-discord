import json
from discord.ext import commands


class Bible:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["passage"])
    async def bible(self, ctx, *, text):
        """<passage> - Prints the specified passage from the Bible"""
        passage = text.strip()
        params = {
            'passage': passage,
            'formatting': 'plain',
            'type': 'json'
        }
        try:
            async with self.bot.session.get("https://labs.bible.org/api", params=params) as resp:
                data = json.loads(await resp.text())[0]
        except Exception:
            await ctx.send("Something went wrong, either you entered an invalid passage or the API is down.")
            raise

        book = data['bookname']
        ch = data['chapter']
        ver = data['verse']
        txt = data['text']
        await ctx.send("\x02{} {}:{}\x02 {}".format(book, ch, ver, txt))


def setup(bot):
    bot.add_cog(Bible(bot))
