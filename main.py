import discord
import os
from discord.ext import commands
from myserver import server_on
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
# ================= TOKEN =================
# Token อยู่ใน render
# ================= ID CHANNEL =================
# ===== ROLE IDs =====
ROLE_1 = 1082668970718527508  # นานาชาติ
ROLE_2 = 1082667309254054008  # Onlyfans
ROLE_3 = 1082667313163157515  # H/ANIME
ROLE_ALL = 1082885961953853540  # เห็นทุกห้อง

OWNER_ROLE = 1049290191778623549
DEVELOPER_ROLE = 1474002697077264424
# ===== QR CODE =====
QR_1 = "https://i.postimg.cc/kXT6hJzP/DH-nana-chat.jpg" # นานาชาติ
QR_2 = "https://i.postimg.cc/FFZ77F99/DH-Onlyfans.jpg" # Onlyfans
QR_3 = "https://i.postimg.cc/521H0HzL/DH-Hanime.jpg" # H/ANIME
# ===== TELEGRAM LINKS =====
LINK_1 = "https://t.me/+ppsrtnXsBAI4ODU1" # นานาชาติ
LINK_2 = "https://t.me/+3QMIoq8e5zg1Zjll" # Onlyfans
LINK_3 = "https://t.me/+tHRrGXsDfk01YTJl" # H/ANIME
# ===== INTENTS =====
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = False

bot = commands.Bot(command_prefix="!", intents=intents)


class LinkButton(discord.ui.View):
    def __init__(self, link):
        super().__init__()

        self.add_item(
            discord.ui.Button(
                label="🔗 ลิงก์กลุ่มกดที่นี่!",
                url=link
            )
        )


class RankSelect(discord.ui.Select):
    def __init__(self):

        options = [

            discord.SelectOption(
                label="กลุ่ม / 𝐕𝐈𝐏・นานาชาติ ꒰79บาท꒱",
                description="สำหรับผู้มียศนี้เท่านั้นหรือซื้อรวม",
                value="rank1",
                emoji=discord.PartialEmoji(
                    name="star1",
                    id=1472134208993497202,
                    animated=True
                )
            ),

            discord.SelectOption(
                label="กลุ่ม / 𝐕𝐈𝐏・𝑶𝒏𝒍𝒚𝒇𝒂𝒏𝒔 ꒰50บาท꒱",
                description="สำหรับผู้มียศนี้เท่านั้นหรือซื้อรวม",
                value="rank2",
                emoji=discord.PartialEmoji(
                    name="star1",
                    id=1472134208993497202,
                    animated=True
                )
            ),

            discord.SelectOption(
                label="กลุ่ม / 𝐕𝐈𝐏・H/ANIME ꒰30บาท꒱",
                description="สำหรับผู้มียศนี้เท่านั้นหรือซื้อรวม",
                value="rank3",
                emoji=discord.PartialEmoji(
                    name="star1",
                    id=1472134208993497202,
                    animated=True
                )
            )
        ]

        super().__init__(
            placeholder="[ 🔒 เลือกกลุ่มที่คุณซื้อเอาไว้ ]",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        if not isinstance(interaction.user, discord.Member):
            return

        role_ids = [role.id for role in interaction.user.roles]

        selected = self.values[0]

        if ROLE_ALL in role_ids:
            allowed = True

        elif selected == "rank1":
            allowed = ROLE_1 in role_ids

        elif selected == "rank2":
            allowed = ROLE_2 in role_ids

        elif selected == "rank3":
            allowed = ROLE_3 in role_ids

        else:
            allowed = False

        if not allowed:

            embed = discord.Embed(
                title="`❌` คุณยังไม่ได้ซื้อยศนี้",
                description=(
                    "```"
                    "กรุณาซื้อยศที่ตรงกับเมนูนี้ก่อนใช้งาน\n"
                    "หากคิดว่าเกิดข้อผิดพลาด กรุณาติดต่อแอดมิน"
                    "```"
                ),
                color=0xFF0000
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )
            return

        # ===== เลือก QR และลิงก์ =====

        if selected == "rank1":
            group_name = "กลุ่ม﹒𝐕𝐈𝐏・นานาชาติ & หมวดหมู่ตลิป"
            qr = QR_1
            link = LINK_1

        elif selected == "rank2":
            group_name = "กลุ่ม﹒𝐕𝐈𝐏・𝑶𝒏𝒍𝒚𝒇𝒂𝒏𝒔/AccLock"
            qr = QR_2
            link = LINK_2

        else:
            group_name = "กลุ่ม﹒𝐕𝐈𝐏・H/ANIME & 3D"
            qr = QR_3
            link = LINK_3

        embed = discord.Embed(
            title=f"📌 {group_name}",
            description=(
                f"{interaction.user.mention}\n\n"
                "> ⏳ Scan QR หรือกดลิ้งก์เพื่อเข้าร่วมกลุ่มที่ซื้อไว้แล้วรอการอนุมัติ"
            ),
            color=0x87CEFA
        )

        embed.set_image(url=qr)

        embed.set_footer(
            text="สแกน QR หรือกดปุ่มด้านล่างนี้เพิ่อเข้าทางลิ้งก์"
        )

        await interaction.response.send_message(
            embed=embed,
            view=LinkButton(link),
            ephemeral=True
        )

class RankView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RankSelect())

async def heartbeat():
    while True:
        print("Bot still running")
        await asyncio.sleep(60)

_initialized = False

@bot.event
async def on_ready():
    global _initialized

    if not _initialized:
        bot.add_view(RankView())
        await bot.tree.sync()
        asyncio.create_task(heartbeat())
        _initialized = True

    print(f"Logged in as {bot.user}")

@bot.event
async def on_disconnect():
    print("❌ Discord Disconnected")

@bot.event
async def on_resumed():
    print("✅ Discord Resumed")

@bot.event
async def on_connect():
    print("🟢 Discord Connected")

@bot.tree.command(name="panel", description="เปิดแผงตัวเลือก")
async def panel(interaction: discord.Interaction):

    role_ids = [
        role.id
        for role in interaction.user.roles
    ] if isinstance(interaction.user, discord.Member) else []

    if (
        OWNER_ROLE not in role_ids
        and DEVELOPER_ROLE not in role_ids
    ):
        await interaction.response.send_message(
            "❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้",
            ephemeral=True
        )
        return

    
    # ตอบยืนยันเฉพาะคนที่ใช้คำสั่ง
    await interaction.response.send_message(
        "✅ เปิดแผงตัวเลือกสำเร็จแล้ว",
        ephemeral=True
    )

    # สร้าง Embed สำหรับแสดงในห้องแชต
    embed = discord.Embed(
        title="<:telegramlogo:1521463301559816212> เข้าร่วมกลุ่ม 𝐓𝐄𝐋𝐄𝐆𝐑𝐀𝐌 ได้เลย!",
        description=(
            "> ** กดเลือกกลุ่มที่คุณซื้อไว้ด้านล่าง 👇 **\n"
            "*<:qrcode:1521467628495962172> ระบบจะแสดง QR และลิงก์ของกลุ่มที่ตรงกับยศของคุณ*"
        ),
        color=0x87CEFA
    )

    # ส่งเป็นข้อความใหม่ในห้องแชต
    await interaction.followup.send(
        embed=embed,
        view=RankView()
    )
# ================= RUN =================

print("Starting Flask...")
server_on()

print("Starting Discord...")
bot.run(os.getenv('TOKEN'))
