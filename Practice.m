number = 113;

while number > 1
    prime = true;
    for comp = 2:number - 1
        if ~mod(number, comp)
            prime = false;
            break;
        end
    end
    if prime
        fprintf('Prime Found: %.0f\n', number);
    end
    number = number - 1;
end