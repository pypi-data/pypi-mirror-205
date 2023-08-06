import pandas as pd
import finlab


class MarketInfo():
    """市場類別
    假如希望開發新的交易市場套用到回測系統，可以繼承 `finlab.market_info.MarketInfo` 來實做新類別。
    """
    @staticmethod
    def get_freq():
        return '1d'

    @staticmethod
    def get_timestamp_name():
        return 'auto'

    @staticmethod
    def get_benchmark():
        """設定對標報酬率的時間序列
        Returns:
          (pd.Series): 時間序列
        Examples:
            | date       |   0050 |
            |:-----------|-------:|
            | 2007-04-23 |   100 |
            | 2007-04-24 |   100.1 |
            | 2007-04-25 |   99 |
            | 2007-04-26 |   98.3 |
            | 2007-04-27 |   99.55 |
        """
        return pd.Series([], index=pd.Index([], dtype='datetime64[ns]'), dtype='float64')

    @staticmethod
    def get_asset_id_to_name():
        """設定對標報酬率的時間序列
        Returns:
          (dict): 股號與股名對照表，ex:`{'2330':'台積電'}`
        """
        return {}

    @staticmethod
    def get_price(trade_at_price, adj=True):
        """取得回測用價格數據
        Args:
           trade_at_price (str): 選擇回測之還原股價以收盤價或開盤價計算，預設為'close'。可選'close'或'open'。
           adj (str): 是否使用還原股價計算。
        Returns:
          (pd.DataFrame): 價格數據
        Examples:
            格式範例

            | date       |   0015 |   0050 |   0051 |   0052 |
            |:-----------|-------:|-------:|-------:|-------:|
            | 2007-04-23 |   9.54 |  57.85 |  32.83 |  38.4  |
            | 2007-04-24 |   9.54 |  58.1  |  32.99 |  38.65 |
            | 2007-04-25 |   9.52 |  57.6  |  32.8  |  38.59 |
            | 2007-04-26 |   9.59 |  57.7  |  32.8  |  38.6  |
            | 2007-04-27 |   9.55 |  57.5  |  32.72 |  38.4  |
            """
        return trade_at_price


class TWMarketInfo(MarketInfo):

    @staticmethod
    def get_freq():
        return '1d'

    @staticmethod
    def get_timestamp_name():
        return 'tw_stock'

    @staticmethod
    def get_benchmark():
        return finlab.data.get('benchmark_return:發行量加權股價報酬指數').squeeze()

    @staticmethod
    def get_asset_id_to_name():
        stock_names = finlab.data._storage.get_stock_names()

        if stock_names == {}:
            categories = finlab.data.get('security_categories')
            new_stock_names = dict(
                zip(categories['stock_id'], categories['name']))
            finlab.data._storage.set_stock_names(new_stock_names)
            stock_names = finlab.data._storage.get_stock_names()

        return stock_names

    @staticmethod
    def get_price(trade_at_price, adj=True):
        if isinstance(trade_at_price, pd.Series):
            return trade_at_price.to_frame()

        if isinstance(trade_at_price, pd.DataFrame):
            return trade_at_price

        if isinstance(trade_at_price, str):
            if trade_at_price == 'volume':
                return finlab.data.get('price:成交股數')

            if adj:
                table_name = 'etl:adj_'
                price_name = trade_at_price
            else:
                table_name = 'price:'
                price_name = {'open': '開盤價', 'close': '收盤價', 'high': '最高價', 'low': '最低價'}[trade_at_price]

            price = finlab.data.get(f'{table_name}{price_name}')
            return price

        raise Exception(f'**ERROR: trade_at_price is not allowed (accepted types: pd.DataFrame, pd.Series, str).')

class USMarketInfo(MarketInfo):

    @staticmethod
    def get_freq():
        return '1d'

    @staticmethod
    def get_timestamp_name():
        return 'us_stock'

    @staticmethod
    def get_benchmark():
        return finlab.data.get('world_index:adj_close')['^GSPC']

    @staticmethod
    def get_asset_id_to_name():
        categories = finlab.data.get('us_tickers')
        stock_names = dict(
            zip(categories['stock_id'], categories['name']))
        return stock_names

    @staticmethod
    def get_price(trade_at_price, adj=True):
        if isinstance(trade_at_price, pd.Series):
            return trade_at_price.to_frame()

        if isinstance(trade_at_price, pd.DataFrame):
            return trade_at_price

        if isinstance(trade_at_price, str):
            if trade_at_price == 'volume':
                return finlab.data.get('us_price:volume')

            if adj:
                table_name = 'us_price:adj_'
                price_name = trade_at_price
            else:
                table_name = 'us_price:'
                price_name = trade_at_price

            price = finlab.data.get(f'{table_name}{price_name}')
            return price

        raise Exception(f'**ERROR: trade_at_price is not allowed (accepted types: pd.DataFrame, pd.Series, str).')