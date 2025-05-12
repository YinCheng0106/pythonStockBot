import discord
import yfinance as yf
import mplfinance as mpf
from discord.ext import commands
from discord import app_commands
from io import BytesIO
from datetime import datetime

class Stock(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="stock", description="searches for a stock")
    @app_commands.describe(symbol="股票代碼", period="時間範圍")
    @app_commands.choices(period=[
        app_commands.Choice(name="1日", value="1d"),
        app_commands.Choice(name="5日", value="5d"),
        app_commands.Choice(name="1個月", value="1mo"),
        app_commands.Choice(name="3個月", value="3mo"),
        app_commands.Choice(name="6個月", value="6mo"),
        app_commands.Choice(name="1年", value="1y"),
        app_commands.Choice(name="2年", value="2y"),
        app_commands.Choice(name="5年", value="5y"),
        app_commands.Choice(name="10年", value="10y"),
        app_commands.Choice(name="整年度", value="ytd"),
        app_commands.Choice(name="最久", value="max")
    ])
    async def stock(self, interaction: discord.Interaction, symbol: str, period: str):
        await interaction.response.defer(ephemeral=False)
        stock = yf.Ticker(symbol)
        try:
            if(stock.info['quoteType'] == 'NONE'):
                await interaction.followup.send(
                    "## 股票代碼錯誤或不存在",
                    ephemeral=True
                )
            else:
                data = stock.history(period=f"{period}")
                price = data['Close'].iloc[-1]
                name = stock.info['longName']
                range = ""
                open_price = data['Open'].iloc[0]
                high_price = data['High'].max()
                low_price = data['Low'].min()
                type = stock.info['quoteType']
                updateTime = datetime.fromtimestamp(stock.info['regularMarketTime'])

                if period == "1d":
                    range = "1日"
                elif period == "5d":
                    range = "5日"
                elif period == "1mo":
                    range = "1個月"
                elif period == "3mo":
                    range = "3個月"
                elif period == "6mo":
                    range = "6個月"
                elif period == "1y":
                    range = "1年"
                elif period == "2y":
                    range = "2年"
                elif period == "5y":
                    range = "5年"
                elif period == "10y":
                    range = "10年"
                elif period == "ytd":
                    range = "整年度"
                elif period == "max":
                    range = "最久"
                else:
                    range = "未知"

                if data.empty:
                    await interaction.followup.send(
                        "## 股票數據下載失敗或沒有數據",
                        ephemeral=True
                    )
                    return
        
                buf = BytesIO()
                mpf.plot(data, type='candle', style='charles', title=symbol, volume=True, savefig=dict(fname=buf, dpi=100, bbox_inches='tight'))
                buf.seek(0)

                file = discord.File(buf, filename=f"{symbol}_chart.png")

                stock_embed = discord.Embed(
                    title = f"{name} ({symbol})",
                    description = f"貨幣：{stock.info['currency']}",
                    color = discord.Color.blue(),
                    timestamp = updateTime
                )
                stock_embed.set_image(url=f"attachment://{symbol}_chart.png")
                stock_embed.set_footer(text="數據來源: Yahoo Finance 更新時間")
                stock_embed.set_author(name=f"股票查詢 ({range})", url="https://tw.stock.yahoo.com")
                stock_embed.add_field(name="開盤價", value=f"{open_price:.2f}", inline=True)
                stock_embed.add_field(name="最高價", value=f"{high_price:.2f}", inline=True)
                stock_embed.add_field(name="最低價", value=f"{low_price:.2f}", inline=True)
                stock_embed.add_field(name="當前價格", value=f"{price:.2f}", inline=True)
                stock_embed.add_field(name="變化幅度", value=f"{((price - open_price) / open_price) * 100:.2f}%", inline=True)
                stock_embed.add_field(name="股票類型", value=f"{type}", inline=True)

                await interaction.followup.send(
                    embed=stock_embed,
                    file=file,
                )
        except Exception as e:
            await interaction.followup.send(
                "## 股票數據下載失敗或沒有數據",
                ephemeral=True
            )
            print(f"Error fetching stock data: {e}")

async def setup(client: commands.Bot):
    await client.add_cog(Stock(client))