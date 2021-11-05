using SIMD

function primes(a, b, n, criba)
  @inbounds for i = 2:Int(floor(sqrt(n)))
    if criba[i]
      for j = i:(n/i)
        criba[Int(i*j)] = false
      end
    end
  end
  criba
end


function main(args)
  i = parse(Int, args[1])
  n = parse(Int, args[2])

  if i == 0
    a = 2
    b = 10^2
    criba = [true for _ in 1:n]
    criba[1] = false
  else
    a = 10^i
    b = 10^2i
    criba = Vector{Bool}(undef, n)
    @inbounds for j = 2:(n+2)
      criba[j] = if args[j] == "1" true else false end
    end
  end
  criba = primes(a, b, n, criba)
  s = ""
  for i in 1:n
    if i > 1
      s *= " "
    end
    s *= string(Int(criba[i]))
  end
  println(s)
end

main(ARGS)