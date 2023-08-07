import pandas as pd
import numpy as np

from io import BytesIO

from capsphere.common.date import MONTH_DICT
from capsphere.domain.output.utils import sort_rows_by_month


def create_worksheet(data: list[list[dict]]) -> BytesIO:

    first_row = 6
    first_col = 1

    average_rcf = _generate_average_rcf(data)

    excel_file = BytesIO()

    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Sheet1')
        writer.sheets['Sheet1'] = worksheet
        worksheet.write('A4', 'Reconstructed Cash Flows')
        worksheet.write('A5', '*Average of 6 months bank statements')

        for output in data:
            index = [d['month'] for d in output]
            df = pd.DataFrame({k: [d[k] for d in output] for k in output[0].keys() if k != 'month'},
                              index=index)

            df = sort_rows_by_month(df)

            df_agg = df.agg(['sum', 'mean'])
            df_agg.index = ['Total', 'Average']
            table = pd.concat([df, df_agg])
            column_settings = [{'header': column} for column in table.columns]
            worksheet.add_table(first_row, first_col, first_row + len(table.index), len(table.columns),
                                {'columns': column_settings})

            table.to_excel(writer, sheet_name='Sheet1', startrow=first_row, startcol=0)
            first_row = first_row + len(index) + 6

        worksheet.write('A' + str(first_row), 'Reconstructed Cash Flow based on 6 months Bank Statements')

        adjusted_row = first_row + 1
        average_rcf.to_excel(writer, sheet_name='Sheet1', startrow=adjusted_row, startcol=0)
        column_settings = [{'header': column} for column in average_rcf.columns]
        worksheet.add_table(adjusted_row, first_col, adjusted_row + len(table.index), len(table.columns),
                            {'columns': column_settings})

    excel_file.seek(0)

    return excel_file


def _generate_average_rcf(rcf_list: list[list[dict]]) -> pd.DataFrame:
    df_list = []

    for inner_list in rcf_list:
        inner_df_list = []
        for d in inner_list:
            df = pd.DataFrame.from_dict(d, orient='index').T
            inner_df_list.append(df)
        inner_result_df = pd.concat(inner_df_list)
        df_list.append(inner_result_df)

    average_rcf = pd.concat(df_list, axis=0, ignore_index=True)
    average_rcf = average_rcf.groupby('month').sum()

    average_rcf = sort_rows_by_month(average_rcf)

    total = average_rcf.sum().rename('Total')
    average = average_rcf.mean().rename('Average')
    total = np.ceil(total * 100) / 100
    average = np.ceil(average * 100) / 100
    average_rcf = average_rcf.T

    average_rcf = pd.concat((average_rcf, total), axis=1)
    average_rcf = pd.concat((average_rcf, average), axis=1)
    average_rcf = average_rcf.T

    return average_rcf
