from translate import Translator

with open("test.txt", "r") as file:
	translator = Translator(to_lang='pt')
	text = file.read()
	translation = translator.translate(text)

with open('translation.txt', 'a') as file:
	file.write(translation)



print('hello')
