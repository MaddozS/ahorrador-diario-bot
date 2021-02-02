msg = {
  'ahorro_text_intro_1': 
    lambda username: 
      f'Ahora *{username}*, me dirás cuánto dinero quieres ahorrar por día\. '
      'Debe estar escrita con números, puedes agregarle el simbolo de dinero pero solo al principio '
      'y si gustas, puede contener decimales\.',
  'ahorro_text_intro_2':
    'Puedes escribir /saltar para usar el modo *AHORRRO ALEATORIO* '
		'el cual consiste en que cada día, tendrás que ahorrar una cantidad aleatoria '
		'dentro de la cantidad de días en los que piensas ahorrar \(en el siguiente paso lo escribirás\)',
  'days_text_intro':
    'Ahora, mándame la cantidad de días que ahorrarás, debe ser mínimo 1',
  'first_saving_text':
    lambda save_per_day: f'Hoy será tu primer día\. Guardarás *{save_per_day}*\.',
  'final_text':
    '¡Ya has terminado tu registro! Hemos guardado toda la información que nos proporcionaste, el día de '
    'mañana te mandaré un mensaje a las 8:00 AM para recordarte guardar tu ahorro.'
}