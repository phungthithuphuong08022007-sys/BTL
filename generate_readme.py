import re
from pathlib import Path
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

README_PATH = Path('README.md')
DATA_PATH = Path('bookstore_inventory.csv')

RESULTS_START = '<!-- RESULTS_START -->'
RESULTS_END = '<!-- RESULTS_END -->'


def load_data():
    df = pd.read_csv(DATA_PATH, encoding='latin1', on_bad_lines='skip')
    df.columns = df.columns.str.strip()
    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    return df.dropna(subset=['month'])


def build_forecast_section(df):
    branches = sorted(df['to'].dropna().unique())
    lines = ['### Dự báo doanh thu 6 tháng tiếp theo', '']
    for branch in branches:
        df_branch = df[df['to'] == branch]
        revenue = (
            df_branch.groupby('month')['extended_retail']
            .sum()
            .resample('MS')
            .sum()
            .fillna(0)
        )
        if len(revenue) < 3:
            continue
        model = ExponentialSmoothing(revenue, trend='add', seasonal=None).fit()
        forecast = model.forecast(6)
        lines.append(f'- `{branch}`')
        for idx, value in forecast.items():
            lines.append(f'  - {idx.strftime("%Y-%m-%d")}: {value:,.2f}')
        lines.append('')
    if len(lines) == 2:
        lines.append('Không đủ dữ liệu để sinh dự báo.')
    return '\n'.join(lines).strip()


def build_risk_section(df):
    sku_stats = (
        df.groupby('sku').agg({'qty': 'sum', 'extended_cost': 'sum'}).reset_index()
    )
    slowest = sku_stats.sort_values('qty', ascending=True).head(5)
    fastest = sku_stats.sort_values('qty', ascending=False).head(5)

    lines = ['### Cảnh báo rủi ro tồn kho', '']
    lines.append('- Top 5 sản phẩm bán chậm nhất (rủi ro đọng vốn):')
    for idx, (_, row) in enumerate(slowest.iterrows(), start=1):
        lines.append(
            f'  {idx}. `{row["sku"]}` - {int(row["qty"])} đơn vị - {row["extended_cost"]:,.2f} $'
        )
    lines.append('')
    lines.append('- Top 5 sản phẩm bán nhanh nhất (rủi ro cháy hàng):')
    for idx, (_, row) in enumerate(fastest.iterrows(), start=1):
        lines.append(
            f'  {idx}. `{row["sku"]}` - {int(row["qty"])} đơn vị - {row["extended_cost"]:,.2f} $'
        )
    return '\n'.join(lines).strip()


def generate_results(df):
    return '\n\n'.join([build_forecast_section(df), build_risk_section(df)])


def update_readme(results_text):
    readme = README_PATH.read_text(encoding='utf-8')
    pattern = re.compile(
        rf'({re.escape(RESULTS_START)})(.*?)(%s)' % re.escape(RESULTS_END),
        flags=re.S,
    )
    if not pattern.search(readme):
        raise RuntimeError('README markers not found. Add RESULTS_START and RESULTS_END to README.')
    updated = pattern.sub(rf'\1\n\n{results_text}\n\n\3', readme)
    README_PATH.write_text(updated, encoding='utf-8')


def main():
    df = load_data()
    results = generate_results(df)
    update_readme(results)
    print('README updated with generated results.')


if __name__ == '__main__':
    main()
