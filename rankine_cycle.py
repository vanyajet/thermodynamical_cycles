import wolframalpha
import string
import ast
import numpy as np

app_id = 'P9W36K-4E6VJW7VL4'
client = wolframalpha.Client(app_id)

#TEMP IN KELVINS, PRESS IN PASCAL

def no_saturation(param, material, pressure, temp):
	query = client.query(param +' of '+ material +' at '+ str(pressure) + ' pascals ' + str(temp) + ' K')
	output = next(query.results).text

	if param == 'enthalpy':
		result = ast.literal_eval(output.replace(' J/kg (joules per kilogram)', ''))

	elif param == 'entropy':
		result = ast.literal_eval(output.replace(' J/(kg K) (joules per kilogram kelvin)', ''))

	elif param == 'density':
		result = ast.literal_eval(output.replace(' kg/m^3 (kilograms per cubic meter)', ''))

	return(result)
# print(no_saturation('density', 'ethane', '2', '400'))
def saturated_pressure(material, temp):
	query = client.query('pressure of '+ material +' at saturation ' + str(temp) + 'K')
	output = next(query.results).text

	result = ast.literal_eval(output.replace(' Pa (pascals)', ''))

	return(result)
# print(saturated_pressure('ethane', '200'))
def saturated_temp(material, pressure):
	query = client.query('temperature of '+ material +' at saturation ' + str(pressure) + 'pascals')
	output = next(query.results).text

	result = ast.literal_eval(output.replace(' K (kelvins)', ''))

	return(result)
# print(saturated_pressure('ethane', '200'))

def saturated(param, state, material, temp):
	query = client.query(param + ' of '+ material +' at saturation ' + str(temp) + 'K')
	output = next(query.results).text

	if param == 'enthalpy':
		result = output.replace(' J/kg (joules per kilogram)', '')
		result1 = result.replace('vapor | ', '')
		result2 = result1.replace('liquid | ', '')
		result3 = result2.replace('\n', ',')
		result4 = result3.split(',')

		if state == 'liquid':
			return(ast.literal_eval(result4[0]))
		elif state == 'vapor':
			return(ast.literal_eval(result4[1]))

	if param == 'entropy':
		result = output.replace(' J/(kg K) (joules per kilogram kelvin)', '')
		result1 = result.replace('vapor | ', '')
		result2 = result1.replace('liquid | ', '')
		result3 = result2.replace('\n', ',')
		result4 = result3.split(',')

		if state == 'liquid':
			return(ast.literal_eval(result4[0]))
		elif state == 'vapor':
			return(ast.literal_eval(result4[1]))
# print(saturated('enthalpy', 'liquid', 'nitrogen', '80'))
def triple_point(material):
	query = client.query('triple point temperature of ' + material)
	output = next(query.results).text

	result = ast.literal_eval(output.replace(' K (kelvins)', ''))

	return(result)
# t_tp = triple_point('ethane')

def rankine(material, T_liq_air, p_liq_air, T0, dT_min, n_pump, n_turb):
	
	T1 = T0 - dT_min

	# print('material ',material)
	# print('T_liq_air ',T_liq_air)
	# print('p_liq_air ',p_liq_air)
	# print('n_pump ',n_pump)
	# print('n_turb ',n_turb)

	# print('dT_min ',dT_min)
	# print('T0 ',T0)
	# print('T1 ',T1)

	T1_11 = T1
	# print ('T1_11 ',T1_11)
	T3_t = T_liq_air + dT_min
	# print ('T3_t ',T3_t)
	T_triple_point = triple_point(material)
	# print ('T_triple_point ',T_triple_point)

	if T3_t > T_triple_point:
		T3 = T3_t
	else:
		T3 = T_triple_point + dT_min

	p3 = saturated_pressure(material, T3)

	if p3 < 5000:
		T3 = T3 + 40 
	
	p3 = saturated_pressure(material, T3)

	# print ('p3 ',p3)
	# print('T3 ',T3)

	h3 = saturated('enthalpy', 'liquid', material, T3)

	# print('h3 ', h3)

	h_vapor_air = saturated('enthalpy', 'vapor', 'nitrogen', T_liq_air)
	# print ('h_vapor_air ',h_vapor_air)
	h_vapor = saturated('enthalpy', 'vapor', material, T3)
	# print ('h_vapor ',h_vapor)
	s_vapor = saturated('entropy', 'vapor', material, T3)
	# print ('s_vapor ',s_vapor)
	s3 = saturated('entropy', 'liquid', material, T3)
	# print ('s3 ',s3)

	s0 = no_saturation('entropy', material, p3, T0)
	# print ('s0 ',s0)
	h0 = no_saturation('enthalpy', material, p3, T0)
	# print ('h0 ',h0)
	rho3 = no_saturation('density', material, p3, T3)
	# print ('rho3 ',rho3)
	

	for dp in np.arange(20, 21, 1):
		#h4 = h3 + (100000*(dp - 1))/(rho3 * n_pump) #убрал р3, так как давление очень маленькое было

		for dp_pp in np.arange(1, 20, 1):

			if dp_pp >= dp:
				continue

			h3_3 = h3 + ((dp_pp * 100000)/(rho3*n_pump))
			p3_3 = p3 + (dp_pp * 100000)

			#print('p3 ', p3)
			# print('p3_3 ', p3_3)

			T3_3 = saturated_temp(material, p3_3)

			# print('T3_3 ', T3_3)

			h3_33 = saturated('enthalpy', 'liquid', material, T3_3)
			h4 = h3_33 + ((dp-dp_pp)* 100000/(rho3*n_pump))
			p4 = p3 + (dp * 100000)


			# print ('h4 ', h4)
			# print('h3_33 ', h3_33)
			# print('h3_3 ', h3_3)

			# p4 = p3+(dp-1)*100000

			# print ('p4 ',p4)

			p1 = p4
			p2 = p3

			# print('p1 ',p1)
			# print('p2 ',p2)

			h1 = no_saturation('enthalpy', material, p1, T1)
			s1 = no_saturation('entropy', material, p1, T1)

			# print ('h1 ',h1)
			# print ('s1 ',s1)

			s_1_1s = s1

			# print ('s_1_1s ',s_1_1s)

			if s1 > s_vapor:
				T_1_1s = T0 - (T0 - T3)*(s0 - s_1_1s)/(s0 - s_vapor)
				h_1_1s = no_saturation('enthalpy', material, p3_3, T_1_1s)
			else:
				x = (s_1_1s - s3)/(s_vapor - s3)
				h_1_1s = h3 * (1-x) + h_vapor * x

			h1_1 = h1 - (h1-h_1_1s)*n_turb

			# print ('h1_1 ', h1_1)

			if h1_1 > h_vapor:
				T1_1 = T0 - (T0 - T3)*(h0 - h1_1)/(h0 - h_vapor)
			else:
				T1_1 = T3

			# print('T1_1 ',T1_1)
			###################################

			h1_11 = no_saturation('enthalpy', material, p3_3, T1_11)
			s1_11 = no_saturation('entropy',  material, p3_3, T1_11)
			# print ('h1_11 ', h1_11)

			s_2s = s1_11

			# print('s1_11 ', s1_11)
			# print('s_2s ', s_2s)

			if s1_11 > s_vapor:
				T_2s = T0 - (T0 - T3)*(s0 - s_2s)/(s0 - s_vapor)
				h_2s = no_saturation('enthalpy', material, p3, T_2s)
			else:
				x = (s_2s - s3)/(s_vapor - s3)
				h_2s = h3 * (1-x) + h_vapor * x

			h2 = h1_11 - (h1_11-h_2s)*n_turb
			# print ('h2 ', h2)

			if h2 > h_vapor:
				T2 = T0 - (T0 - T3)*(h0 - h2)/(h0 - h_vapor)
			else:
				T2 = T3

			###################################


			T_air_max = T2 - dT_min
			# T_air_max = T1_1 - dT_min 
			# print ('T2 ',T2)
			# print ('T_air_max ',T_air_max)

			if T_air_max > T_liq_air:
				h_air_max = no_saturation('enthalpy', 'nitrogen', p_liq_air, T_air_max)
			else:
				h_air_max = h_vapor_air

			# воздух
			h_liq_air = saturated('enthalpy', 'liquid', 'nitrogen', T_liq_air)
			# print ('h_air_max ',h_air_max)
			# print ('h_liq_air ',h_liq_air)

			alpha = (h3_33 - h3_3)/(h1_1 - h3_3)

			G = (h_air_max - h_liq_air)/(h2 - h3)
			# print ('G ', G)
			# print('h1 ', h1)
			
			N = G * (h1 - h1_1 - h4 + h3_33) + (1-alpha) * G * (h1_11 - h2 - h3_3 + h3)

			# N = G * (h1 - h2 - h4 + h3).

			# print('dp ',dp)
			# print('dp_pp ',dp_pp)
			# print('alpha ',alpha)
			# print('N ',N)



			print(dp,dp_pp,alpha,N)

rankine('ethane', 78, 1, 293, 5, 0.92, 0.89)


#2 1 -282055.24973161623
#3 1 -332481.4484220481
#3 2 -1095448.7370505594
#4 1 -376297.8940550039

#2 1 -281680.5343329346
#3 1 -332148.78146943543
