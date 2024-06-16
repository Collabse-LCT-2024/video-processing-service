import unittest
import numpy as np

from embedders.labse_embedder import LabseEmbedder


class TestLabseEmbedder(unittest.TestCase):
    def setUp(self):
        self.embedder = LabseEmbedder()
        self.test_texts = [
            "Не знали о существовании Lexus RX 350? Сейчас расскажу. В основе абсолютно новая платформа, что дало изменения в габаритах и двигателе. Здесь у нас теперь 4-поршневая тормозная система 440 мм. Комплектация F-Sport, а это здесь, здесь, здесь и здесь. Это отличительные особенности Lexus RX F-Sport. Здесь у нас 14-дюймовый дисплей, который вот так вот поддерживает всю навигационную систему. Цифровая приборная панель, проекционный дисплей и нефиксируемый шифтер коробки передач. Имеется складываемый и раскладываемый второй ряд Объем багажника 700 литров И имеется открытие и закрытие с ноги А это второй ряд сидений Lexus RX здесь места стало больше Трехзонный климат-контроль и вентиляция задних сидений А также имеется подогрев Здесь теперь нет мотора V6, турбо-четверка С двигателем 279 л.с. Как вам такой Lexus RX?"
        ]

    def test_embed_returns_normalized_embeddings(self):
        embeddings = self.embedder.embed(self.test_texts)
        norm = np.linalg.norm(embeddings)
        self.assertAlmostEqual(norm, 1.0, places=6)

        print(embeddings)


if __name__ == "__main__":
    unittest.main()
