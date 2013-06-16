
Dir.chdir(__dir__)
$dir = "1112"
fnn = '1112_all_info.txt'
Dir.mkdir $dir rescue nil

data = File.binread(fnn)
x = Regexp.new(("\x80".."\xff").to_a.join('|').b)
data = data.gsub x, ''

$fn = ''
LS = []

data.each_line { |line|  
  if /^# (?<x>.+)$/ =~ line
    if !$fn.empty?
      if !LS.join.strip.empty?
        puts "#{$fn}    created"
        File.write("#{$dir}/#{$fn}", LS.join)
      else
        puts "#{$fn}          SKIP EMPTY."
      end
    end
    
    $fn = x.chomp
    LS.clear
  else
    LS << line
  end
  
}

#last
if !LS.join.strip.empty?
  puts "#{$fn}    created"
  File.write("#{$dir}/#{$fn}", LS.join)
else
  puts "#{$fn}          SKIP EMPTY."
end
