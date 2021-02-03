from datetime import datetime


class N19Parser(object):
    def parse(self, data):
        lines = data.decode('utf-8').split("\n")
        presenter_header_line = next(line for line in lines if line[0:2] == '21')
        name = presenter_header_line[123:158]
        creditor_header_line = next(line for line in lines if line[0:2] == '22')
        payment_return = self.parse_payment_return(creditor_header_line)
        payment_return['name'] = name
        transaction_lines = [line for line in lines if line[0:2] == '23']
        for transaction_line in transaction_lines:
            self.parse_payment_transaction(
                payment_return['transactions'], transaction_line
            )
        subno = 0
        for transaction in payment_return['transactions']:
            subno += 1
            transaction['unique_import_id'] = (
                payment_return['name'] + " - " + str(subno).zfill(4)
            )
        return payment_return

    def parse_payment_return(self, line):
        payment_return = {
            'date': datetime.strptime(line[45:53], '%Y%m%d'),
            'name': line[123:158],
            'account_number': line[265:299].strip(),
            'transactions': [],
        }
        return payment_return

    def parse_payment_transaction(self, transactions, line):
        transaction = {
            'reference': line[10:45].strip(),
            'reason_code': line[593:597],
            'amount': (float(line[88:97]) + (float(line[97:99]) / 100)),
            'concept': line[441:581].strip(),
            'partner_name': line[126:196].strip(),
            'account_number': line[411:445].strip(),
            'raw_import_data': line,
            'mandate': line[45:80].strip(),
        }
        transactions.append(transaction)
