import pyromat as pm
#pm.config - расскажет какие единицы измерения мы используем
#давление - kpa, темп - K, энергия - kJ

#p1 10kpa ; p2 2mpa

pm.config["unit_pressure"] = "kPa"

# 1-2 - pump, 2-3 - boiler, 3-4 - turbine, 4-1 condenser

#multi-phase water

# INITIAL DATA

mp_water = pm.get("mp.H2O")

p1 = 10
p2 = 2000

# PUMP

# объем (v) - обратное от плотности.
#Плотность запрашиваем от mp_water; .ds - плотность;
#(p=p1) - при давлении; [0] - жидкость при насыщении [1] - пар при насыщении

v = 1/mp_water.ds(p=p1)[0]

#w_p - work required by pump

w_p = v*(p2-p1)

print(f"Work required by pump: {round(float(w_p),2)} kJ/kg")

h1 = mp_water.hs(p=p1)[0]

h2 = h1+w_p

print(f"h2 = {round(float(h2),2)} kJ/kg")

# BOILER

#pressure after boiler = pressure before boiler
# h3 = mp_water.hs(p=p3) [1] - because x = 1 after boiler(steam)

p3 = p2
h3 = mp_water.hs(p=p3)[1]
s3 = mp_water.ss(p=p3)[1]
q_H = h3-h2

print(f"Heat input by boiler = {round(float(q_H),2)} kJ/kg")

# TURBINE

p4 = p1 
s4 = s3

#далее идет расчет степени сухости пара по встроенной функции T_s
#принимающую в себя энтропию и давление(функция возвращает то что попросить)
#quality=True - это просьба вернуть нам степень сухости по результату выполнения функции
x = mp_water.T_s(s=s4, p=p4, quality=True)[1]
h4 = mp_water.h(p=p4, x=x)

w_t = h3-h4

print(f"Work generated by turbine = {round(float(w_t),2)} kJ/kg")

# CONDENSER

q_L = h4-h1
print(f"Work rejected by condenser = {round(float(q_L),2)} kJ/kg")

eff_th = (w_t-w_p)/q_H * 100

print(f"Thermal efficiency = {round(float(eff_th),2)} %")



