drop table if exists reports;
create table reports (
    code text,
    rdate date,
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
    roa float, -- 당기순이익 / 자산총계
    gpa float, -- 매출총이익 / 자산총계
    reg_date date,
    upd_date date,
    primary key (code, rdate)
);

drop table if exists companies;
create table companies (
    code text primary key,
    market text,
    company text not null,
    ind_code text, -- 산업코드
    industry text, -- 산업명
    reg_date date,
    upd_date date
);

drop table if exists prices;
create table prices (
    code text,
    sdate date,
    start integer,
    max integer,
    min integer,
    close integer,
    volume integer,
    shares integer, -- 주식수
    market_cap integer, -- 시가총액
    per float, -- 시가총액 / 당기순이익
    psr float, -- 시가총액 / 매출액
    pcr float, -- 시가총액 / 영업현금흐름
    pbr float, -- 시가총액 / 자본총계
    reg_date date,
    upd_date date,
    primary key (code, sdate)
);
