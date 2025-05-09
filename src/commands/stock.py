import discord
import yfinance as yf
import mplfinance as mpf
from discord.ext import commands
from discord import app_commands
from io import BytesIO

class Stock(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="stock", description="searches for a stock")
    @app_commands.describe(symbol="The stock to search for")
    async def stock(self, interaction: discord.Interaction, symbol: str):
        await interaction.response.defer(ephemeral=True)
        stock = yf.Ticker(symbol)
        if(stock.info['quoteType'] == 'NONE'):
            await interaction.followup.send(
                "## 股票代碼錯誤或不存在",
                ephemeral=True
            )
        else:
            data = stock.history(period="1mo")
            price = data['Close'].iloc[-1]

            if data.empty:
                await interaction.followup.send(
                    "## 股票數據下載失敗或沒有數據",
                    ephemeral=True
                )
                return
        
            price = data['Close'].iloc[-1]
            
            buf = BytesIO()
            mpf.plot(data, type='candle', style='charles', title=symbol, volume=True, savefig=dict(fname=buf, dpi=100, bbox_inches='tight'))
            buf.seek(0)

            file = discord.File(buf, filename=f"{symbol}_chart.png")

            stock_embed = discord.Embed(
                title=f"{symbol}",
                description=f"價格: {price:.2f}",
                color=discord.Color.blue()
            )
            stock_embed.set_image(url=f"attachment://{symbol}_chart.png")
            stock_embed.set_footer(text="數據來源: Yahoo Finance")
            stock_embed.set_author(name="股票查詢", url="https://tw.stock.yahoo.com")

            await interaction.followup.send(
                embed=stock_embed,
                file=file,
                ephemeral=True
            )
        

async def setup(client: commands.Bot):
    await client.add_cog(Stock(client))