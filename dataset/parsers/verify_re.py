import re


# end_of_sent = re.compile(r'(?<=[0-9][^(v.)])\)?\. (?=[A-ZА-Я])', re.UNICODE)
end_of_sent = re.compile(r'(?<=[\w0-9])[)"»”]?\. (?=[A-ZА-Я])', re.UNICODE)
input_s = 'Крім того, під час провадження у районному суді заявник пояснив, що отримав кошти за договором приватної позики, і надав документи у підтвердження цих фактологічних тверджень (див. пункт 9). Органи державної влади прямо не розглянули це питання, оскільки вони, вочевидь, вважали, що воно не стосувалося справи, принаймні застосування заходу у вигляді конфіскації'

res = end_of_sent.split(input_s)
for r in res:
    print(r)
assert len(res) == 2, len(res)

input_s2 = 'Другий аспект підходу Суду полягає в тому, що застосовується критерій доведеності «поза розумним сумнівом». Разом з цим цей критерій не співпадає з критерієм національних правових систем, в яких він застосовується'
res2 = end_of_sent.split(input_s2)
for r in res2:
    print(r)
assert len(res2) == 2, len(res2)
