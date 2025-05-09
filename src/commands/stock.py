import discord
import yfinance as yf
import mplfinance as mpf
from discord.ext import commands
from discord import app_commands
from io import BytesIO

class Stock(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="apple", description="Sends a list of stocks")
    async def apple(self, interaction: discord.Interaction):
        apple = yf.Ticker("AAPL")
        data = apple.history(period="1d")
        price = data['Close'].iloc[-1]
        print(data)
        await interaction.response.send_message(
            f"Apple stock data: {price:.2f}",
            ephemeral=True
        )

    @app_commands.command(name="stock", description="searches for a stock")
    @app_commands.describe(symbol="The stock to search for")
    async def stock(self, interaction: discord.Interaction, symbol: str):
        try:
            if not symbol.isalpha():
                await interaction.response.send_message("請輸入有效的股票代碼。", ephemeral=True)
                return

            stock = yf.Ticker(symbol)
            data = stock.history(period="1mo")
            if data.empty:
                await interaction.response.send_message("股票數據下載失敗或沒有數據。", ephemeral=True)
                return
        except Exception as e:
            await interaction.response.send_message(f"發生錯誤: {str(e)}", ephemeral=True)
            return
        stock = yf.Ticker(symbol)
        data = stock.history(period="1mo")
        price = data['Close'].iloc[-1]
        if data.empty:
            await interaction.response.send_message("股票數據下載失敗或沒有數據。", ephemeral=True)
            return
    
        price = data['Close'].iloc[-1]
        
        buf = BytesIO()
        mpf.plot(data, type='candle', style='charles', title=symbol, volume=True, savefig=dict(fname=buf, dpi=100, bbox_inches='tight'))
        buf.seek(0)

        file = discord.File(buf, filename=f"{symbol}_chart.png")

        stock_embed = discord.Embed(
            title=f"{symbol} 股票資訊",
            description=f"價格: {price:.2f}",
            color=discord.Color.blue()
        )
        stock_embed.set_image(url=f"attachment://{symbol}_chart.png")

        await interaction.response.send_message(
            embed=stock_embed,
            file=file,
            ephemeral=True
        )
        

async def setup(client: commands.Bot):
    await client.add_cog(Stock(client))