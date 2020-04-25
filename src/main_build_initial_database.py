import financial_reports as step01
import financial_reports_fill_missing_data as step02
import stock_prices_github as step03
import stock_prices_krx as step04
import investment_indicators as step05
import economic_indicators as step06


if __name__ == "__main__":
    step01.do_main_proc_for_financial_reports()
    step02.do_main_proc_for_financial_reports_fill_missing_data()
    step03.do_main_proc_to_update_stock_prices_github()
    step04.do_main_proc_to_update_stock_prices_krx()
    step05.do_main_proc_to_update_investment_indicators()
    step06.do_main_proc_to_update_economic_indicators()
    print('Done')
