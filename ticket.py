import discord
from discord.ext import commands
import asyncio

STAFF_ROLE_ID = 1510432038107217992
CATEGORY_ID = 1510448421780062308


class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Fechar Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.red,
        custom_id="close_ticket"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(
            "🔒 Ticket será fechado em 5 segundos.",
            ephemeral=True
        )

        await asyncio.sleep(5)
        await interaction.channel.delete()


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Fazer Anúncio",
        emoji="📢",
        style=discord.ButtonStyle.green,
        custom_id="anuncio_ticket"
    )
    async def anuncio_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        print("BOTÃO ANÚNCIO CLICADO")

        guild = interaction.guild
        user = interaction.user

        category = guild.get_channel(CATEGORY_ID)
        staff_role = guild.get_role(STAFF_ROLE_ID)

        canal_existente = discord.utils.get(
            guild.channels,
            name=f"anuncio-{user.id}"
        )

        if canal_existente:
            return await interaction.response.send_message(
                f"Você já possui um ticket aberto: {canal_existente.mention}",
                ephemeral=True
            )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            staff_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        }

        print("VAI CRIAR O CANAL")

        try:
            canal = await guild.create_text_channel(
                name=f"anuncio-{user.id}",
                category=category,
                overwrites=overwrites
            )

            print("CANAL CRIADO")

        except Exception as e:
            print("ERRO AO CRIAR CANAL:")
            print(e)

            return await interaction.response.send_message(
                "❌ Erro ao criar o canal. Contate um administrador.",
                ephemeral=True
            )

        embed = discord.Embed(
            title="📢 Ticket de Anúncio",
            description=(
                "**Preencha as informações abaixo:**\n\n"
                "📌 Título:\n"
                "📝 Descrição:\n"
                "🖼️ Imagens:\n"
                "📞 Contato:"
            ),
            color=discord.Color.green()
        )

        await canal.send(
            f"{user.mention} {staff_role.mention}",
            embed=embed,
            view=CloseTicketView()
        )

        await interaction.followup.send(
            f"✅ Ticket criado: {canal.mention}",
            ephemeral=True
        )

    @discord.ui.button(
        label="Fazer Denúncia",
        emoji="🚨",
        style=discord.ButtonStyle.red,
        custom_id="denuncia_ticket"
    )
    async def denuncia_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        print("BOTÃO DENÚNCIA CLICADO")

        guild = interaction.guild
        user = interaction.user

        category = guild.get_channel(CATEGORY_ID)
        staff_role = guild.get_role(STAFF_ROLE_ID)

        print("Categoria:", category)
        print("Cargo:", staff_role)

        canal_existente = discord.utils.get(
            guild.channels,
            name=f"denuncia-{user.id}"
        )

        if canal_existente:
            return await interaction.response.send_message(
                f"Você já possui um ticket aberto: {canal_existente.mention}",
                ephemeral=True
            )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            staff_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        }

        canal = await guild.create_text_channel(
            name=f"denuncia-{user.id}",
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🚨 Ticket de Denúncia",
            description=(
                "**Informe os dados abaixo:**\n\n"
                "👤 ID do denunciado:\n"
                "📋 Motivo:\n"
                "📸 Provas:\n"
                "📅 Data do ocorrido:"
            ),
            color=discord.Color.red()
        )

        await canal.send(
            f"{user.mention} {staff_role.mention}",
            embed=embed,
            view=CloseTicketView()
        )

        await interaction.followup.send(
            f"✅ Ticket criado: {canal.mention}",
            ephemeral=True
        )


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def painel(self, ctx):

        embed = discord.Embed(
            title="🎫 Central de Atendimento",
            description=(
                "Selecione uma opção abaixo.\n\n"
                "📢 Fazer Anúncio\n"
                "🚨 Fazer Denúncia"
            ),
            color=discord.Color.blurple()
        )

        await ctx.send(
            embed=embed,
            view=TicketView()
        )


async def setup(bot):
    await bot.add_cog(Ticket(bot))
    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())