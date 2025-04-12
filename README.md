# 🏷️ ProfileStamp

**ProfileStamp** é uma biblioteca Python para gerar **selos personalizados** (stamps) em fotos de perfil, ideal para uso em redes sociais, campanhas de marketing, eventos ou comunidades online.

Com suporte a textos curvados, cores personalizadas, degradês e mascaramento em círculo, essa biblioteca é perfeita para criar **imagens impactantes e com identidade visual** forte para seus seguidores.

---

## 🚀 Instalação

```bash
git clone https://github.com/cleitonleonel/ProfileStamp.git
```

> Requer: `Pillow` e `numpy`

---

## 🎨 Exemplos de Uso

```python
from app.pystamp import generate_profile_stamp

generate_profile_stamp(
    profile_path="minha_foto.png",
    stamp_text="#PROFILESTAMP",
    output_path="com_selo.png",
    stamp_color="blue",
    text_color="white",
    gradient=True
)
```

### Resultado:

<img src="/src/img/stamp.png" width="250">

---

## ⚙️ Parâmetros

| Parâmetro      | Tipo     | Descrição                                                                 |
|----------------|----------|---------------------------------------------------------------------------|
| `profile_path` | `str`    | Caminho para a imagem de perfil.                                          |
| `stamp_text`   | `str`    | Texto que será curvado ao redor da imagem.                                |
| `output_path`  | `str`    | Caminho de saída da imagem gerada.                                        |
| `stamp_color`  | `str` ou `tuple` | Cor do selo. Pode ser uma string como `"blue"` ou uma tupla RGBA.        |
| `text_color`   | `str` ou `tuple` | Cor do texto curvado. Igual ao formato da cor do selo.                   |
| `gradient`     | `bool`   | Se `True`, aplica um degradê suave ao selo.                               |
| `font_path`    | `str`    | Caminho para a fonte (opcional). Padrão: DejaVuSans-Bold.                 |
| `font_size`    | `int`    | Tamanho da fonte do texto.                                                |

---

## 🧩 Cores Pré-definidas

```python
"purple", "blue", "light_blue", "green", "light_green",
"red", "orange", "yellow", "pink", "gray",
"black", "white"
```

Você também pode usar tuplas RGBA personalizadas como: `(255, 0, 0, 255)`.

---

## 🛠️ To-Do

- [ ] Adicionar suporte a múltiplos estilos de selo (ex: quadrado, borda dupla).
- [ ] Permitir posicionamento de textos extras.
- [ ] Geração em lote.

---

## 🤝 Contribuindo

Sinta-se livre para abrir *issues* ou enviar *pull requests*! Toda ajuda é bem-vinda.

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja `LICENSE` para mais detalhes.

---

## 💡 Inspiração

Projetado para desenvolvedores e comunidades que querem marcar presença com estilo nas redes. Ideal para perfis engajados em causas, eventos ou linguagens de programação. 😉
