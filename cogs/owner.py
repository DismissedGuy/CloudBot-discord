import io
import os
import traceback
import textwrap
from contextlib import redirect_stdout
import copy
from discord.ext import commands
import discord


class Owner:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author) or ctx.author.id == 311869975579066371

    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message
        }

        env.update(globals())

        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(hidden=True)
    async def runas(self, ctx, who: discord.Member, *, cmd):
        """Run a command impersonating another user."""
        cmd = cmd.strip('`')

        fake_msg = copy.copy(ctx.message)

        # msg._update handles clearing cached properties
        fake_msg._update(ctx.message.channel, dict(
            content=ctx.prefix + cmd))
        fake_msg.author = who
        new_ctx = await ctx.bot.get_context(fake_msg)
        await ctx.bot.invoke(new_ctx)

    @commands.command(hidden=True)
    async def reload(self, ctx):
        """Unloads all extensions and loads them again"""
        current_extensions = list(self.bot.cogs.values())
        new_extensions = [f.rstrip('.py') for f in os.listdir('cogs') if os.path.isfile(f'cogs/{f}')]
        res = ''

        for ext in current_extensions:
            self.bot.unload_extension(ext.__module__)

        for ext in new_extensions:
            try:
                self.bot.load_extension(f'cogs.{ext}')
                res += f'✅ - {ext}\n'
            except Exception as e:
                res += f'❌ - {ext}\n> {e}\n'
        await ctx.send(f'```\n{res}\n```')


def setup(bot):
    bot.add_cog(Owner(bot))
