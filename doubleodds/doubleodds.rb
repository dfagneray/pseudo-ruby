CONST = 5
numbers = [1, 2, 3, 4, 5]
doubled_odds = numbers.select{ |n| n % 2 == 1 }.map{ |n| n * 2 }
p doubled_odds

