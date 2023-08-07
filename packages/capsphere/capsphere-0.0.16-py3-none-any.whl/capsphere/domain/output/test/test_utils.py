import unittest
import pandas as pd

from capsphere.domain.output.utils import sort_rows_by_month


class TestUtils(unittest.TestCase):

    data = {'start_balance': [83407.48, 49863.77],
            'end_balance': [49863.77, 50063.57],
            'total_debit': [26702.45, 640.08],
            'total_credit': [70015.86, 40640.00],
            'average_debit': [3500.76, 160.04],
            'average_credit': [7001.59, 40.00]}

    order_1 = ['Aug 2022', 'Sep 2022']
    order_2 = ['Sep 2022', 'Aug 2022']
    order_3 = ['Aug 2022', 'Aug 2022']
    order_4 = ['Aug 2022', 'Aug 2021']
    order_5 = ['Aug 2022', 'Sep 2021']
    order_6 = ['Aug 2022', 'Sep 2023']

    def test_row_order(self):
        df_1 = pd.DataFrame(self.data, index=self.order_1)
        df_2 = pd.DataFrame(self.data, index=self.order_2)
        df_3 = pd.DataFrame(self.data, index=self.order_3)
        df_4 = pd.DataFrame(self.data, index=self.order_4)
        df_5 = pd.DataFrame(self.data, index=self.order_5)
        df_6 = pd.DataFrame(self.data, index=self.order_6)

        output_1 = sort_rows_by_month(df_1)
        output_2 = sort_rows_by_month(df_2)
        output_3 = sort_rows_by_month(df_3)
        output_4 = sort_rows_by_month(df_4)
        output_5 = sort_rows_by_month(df_5)
        output_6 = sort_rows_by_month(df_6)

        self.assertEqual(output_1.index.values.tolist(), ['Aug 2022', 'Sep 2022'])
        self.assertEqual(output_2.index.values.tolist(), ['Aug 2022', 'Sep 2022'])
        self.assertEqual(output_3.index.values.tolist(), ['Aug 2022', 'Aug 2022'])
        self.assertEqual(output_4.index.values.tolist(), ['Aug 2021', 'Aug 2022'])
        self.assertEqual(output_5.index.values.tolist(), ['Sep 2021', 'Aug 2022'])
        self.assertEqual(output_6.index.values.tolist(), ['Aug 2022', 'Sep 2023'])

