import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    receipt = file.read()


lines = [line.strip() for line in receipt.split('\n') if line.strip()]


# 1 Extract all prices from the receipt

all_prices = []
price_pattern = r'\b\d+(?:\s\d+)*(?:[.,]\d{2})\b'

for i in range(len(lines)):
    if re.match(r'^\d+\.$', lines[i]):
        price_line = lines[i + 2] 
        price_match = re.findall(price_pattern, price_line)
        if price_match:
            
            clean_str = price_match[-1].replace(" ", "").replace(',', '.')
            all_prices.append(float(clean_str))


# 2 Find all product names

products_name = []
product_number_pattern = r'^\d+\.$'

for i in range(len(lines)):
    if re.search(product_number_pattern, lines[i]):
        name = lines[i + 1]
        products_name.append(name)

# 3 Calculate total amount

total_sum = sum(all_prices)
total_calculated = round(total_sum, 2)
print(total_calculated)

# 4 Extract date and time information

receipt_date = None
receipt_time = None

date_pattern = r'\b\d{2}\.\d{2}\.\d{4}\b'
time_pattern = r'\b\d{2}:\d{2}:\d{2}\b'

for line in lines:
    if "Время:" in line:
        date_match = re.search(date_pattern, line)
        time_match = re.search(time_pattern, line)
        
        if date_match:
            receipt_date = date_match.group(0) 
            receipt_time = time_match.group(0)


print(receipt_date)
print(receipt_time)


# 5 Find payment method

payment_method = None

card_pattern = r'Банковская\s+карта'
cash_pattern = r'Наличные'

for line in lines:
    if re.search(card_pattern, line, re.IGNORECASE):
        payment_method = "Банковская карта"
        break
    elif re.search(cash_pattern, line, re.IGNORECASE):
        payment_method = "Наличные"
        break


print(payment_method)

# 6  Save as JSON file

receipt_data = {
    "prices": all_prices,
    "products": products_name,
    "total": total_calculated,
    "date": receipt_date,
    "time": receipt_time,
    "payment_method": payment_method
}

json_string = json.dumps(receipt_data, indent=4, ensure_ascii=False)



print(json_string)




