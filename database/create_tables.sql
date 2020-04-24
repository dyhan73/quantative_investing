drop table if exists reports;
create table reports (
    code text not null,
    rdate date not null,
    total_assets integer,   -- 자산총계
    current_assets integer, -- 유동자산
    total_liabilities integer, -- 부채총계
    total_equity integer, -- 자본총계
    net_sales integer, -- 매출액
    cost_of_sales integer, -- 매출원가
    gross_profit integer, -- 매출총이익
    operating_income integer, -- 영업이익
    ongoing_operating_income integer, -- 당기순이익
    cash_flows_from_operatings integer, -- 영업현금흐름
    current_ratio float, -- 유동비율
    debt_to_equity_ratio float, -- 부채비율
    q1_net_sales integer,
    q1_gross_profit integer,
    q1_ongoing_operating_income integer,
    q4_net_sales integer,
    q4_gross_profit integer,
    q4_ongoing_operating_income integer,
    stock_shares integer, -- 주식수

    roa float, -- 당기순이익 / 자산총계
    gpa float, -- 매출총이익 / 자산총계
    reg_date date,
    upd_date date,
    primary key (code, rdate)
);

drop table if exists companies;
create table companies (
    code text not null primary key,
    market text,
    company text not null,
    ind_code text, -- 산업코드
    industry text, -- 산업명
    reg_date date,
    upd_date date
);

drop table if exists prices;
create table prices (
    code text not null,
    sdate date not null,
    open integer,
    high integer,
    low integer,
    close integer,
    trading_volume integer, -- 거래량
    trading_value integer,  -- 거래대금
    adj_close integer,
    movement integer,  -- 대비 (전일대비)
    movement_ratio float,  -- 등락률
    total_shares integer, -- 주식수
    market_cap integer, -- 시가총액
    market_ratio float, -- 시가총액비중(%)
    foreign_shares integer,  -- 외국인 보유주식수
    foreign_ratio float,  -- 외국인 지분율(%)
    calc_market_cap integer, -- 가격 * 보고서주식수로 계산된 시가총액
    per float, -- 시가총액 / 당기순이익
    psr float, -- 시가총액 / 매출액
    pcr float, -- 시가총액 / 영업현금흐름
    pbr float, -- 시가총액 / 자본총계
    reg_date date,
    upd_date date,
    primary key (code, sdate)
);
-- drop index ix_prices_date;
create index ix_prices_date on prices(sdate);


-- alter table reports add q1_net_sales integer;
-- alter table reports add q1_gross_profit integer;
-- alter table reports add q1_ongoing_operating_income integer;
-- alter table reports add q4_net_sales integer;
-- alter table reports add q4_gross_profit integer;
-- alter table reports add q4_ongoing_operating_income integer;
-- alter table reports add stock_shares integer;
-- alter table prices add calc_market_cap integer;