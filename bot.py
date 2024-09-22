import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # ให้บอทสามารถอ่านข้อความได้
intents.members = True  # ให้บอทเข้าถึงข้อมูลสมาชิก

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

def check_age(id_card):
    """ฟังก์ชันตรวจสอบอายุจากเลขบัตรประชาชน"""
    if len(id_card) == 13 and id_card.isdigit():
        birth_year = int(id_card[1:3]) + 1900  # ปรับให้ตรงกับรูปแบบเลขบัตรของคุณ
        current_year = 2024  # แก้ไขปีตามปัจจุบัน
        age = current_year - birth_year

        return age >= 16  # ถ้าอายุมากกว่าหรือเท่ากับ 16 ปี ให้คืนค่า True
    return False  # ถ้าไม่ผ่าน

@bot.command()
async def verify(ctx, *, id_card: str = None):
    """ตรวจสอบหมายเลขบัตรประชาชน"""
    if id_card is None:
        await ctx.send("กรุณากรอกเลขบัตรประชาชนของคุณ โดยใช้คำสั่ง !verify <เลขบัตรประชาชน>")
        return

    await ctx.send(f"เราได้ส่งให้คุณยืนยันแล้วใน DM, {ctx.author.mention}")

    try:
        if check_age(id_card):
            await ctx.author.send("คุณผ่านการยืนยันแล้ว! ยินดีด้วย")
            await ctx.author.send(file=discord.File('path/to/success.gif'))  # เปลี่ยนเป็น path ของ GIF ยืนยันสำเร็จ

            # เพิ่มยศ (Role) ให้ผู้ใช้
            role = discord.utils.get(ctx.guild.roles, name="Verified")  # ใส่ชื่อยศที่ต้องการ
            if role:
                await ctx.author.add_roles(role)
                await ctx.author.send(f"คุณได้รับยศ '{role.name}' แล้ว!")
            else:
                await ctx.author.send("ไม่พบยศที่ต้องการเพิ่ม โปรดตรวจสอบชื่อยศ")
        else:
            await ctx.author.send("คุณไม่ผ่านการยืนยัน เนื่องจากอายุต่ำกว่า 16 ปี")
            await ctx.author.send(file=discord.File('path/to/failure.gif'))  # เปลี่ยนเป็น path ของ GIF ยืนยันไม่ผ่าน
    except Exception as e:
        await ctx.author.send("มีข้อผิดพลาดในการตรวจสอบ โปรดลองใหม่อีกครั้ง")
        print(f"Error in command 'verify': {e}")  # แสดงข้อผิดพลาดใน console

TOKEN = os.getenv('DISCORD_TOKEN')  # ใช้ Environment Variable สำหรับ Token
bot.run(TOKEN)  # รันบอท
