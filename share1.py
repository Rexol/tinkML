class ShareState:
    def __init__(self, row):
        (self.date, self.price, self.time) = self.convert_row(row)

    # This function parses our table's row into 3 variables.
    @staticmethod
    def convert_row(row):
        row = row.replace('\n','')
        splited_row = row.split(',')
        (date, time) = map(int, (splited_row[1], splited_row[2]))
        price = float(splited_row[3])
        return date, price, time

def gen_min_arr(fname):
    a = []
    with open(fname) as file:
        next(file)
        for index, row in enumerate(file.readlines()):
            current_share_state = ShareState(row)
            if index == 0:
                a.append(current_share_state)
                continue

            previous_min_share_state = a[index - 1]
            if current_share_state.price < previous_min_share_state.price:
                a.append(current_share_state)

            else:
                a.append(previous_min_share_state)
    return a

if __name__ == '__main__':
    min_price_arr = gen_min_arr('new.csv')
    buy = []
    sell = []
    with open('new.csv') as file:
        next(file)
        maxprofit = 0
        for index, row in enumerate(file.readlines()):
            current_share_state = ShareState(row)
            min_share_state = min_price_arr[index]
            if index == 0:
                continue

            if current_share_state.price - min_share_state.price > maxprofit:
                buy = min_share_state
                sell = current_share_state
                maxprofit = current_share_state.price - min_share_state.price


    print(f'You need to buy shares at {buy.date} {buy.time} with price {buy.price:.2f}')
    print(f'And you need to sell them at {sell.date} {sell.time} with price {sell.price:.2f}')
    print(f'Your profit would be {sell.price - buy.price:.2f} per share')