from deep_translator import GoogleTranslator

translatot = GoogleTranslator(source="auto", target="uk")

input_text_from_user = input("Введіть текст, який потрібно перекласти: ")

text_after_translete = translatot.translate(input_text_from_user)

print("Переклад: ", text_after_translete)



