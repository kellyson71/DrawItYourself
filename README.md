# DrawItYourself 🎨

Uma rede social dedicada para artistas compartilharem suas criações digitais. Compartilhe desenhos, histórias em quadrinhos e conecte-se com outros artistas!

## ✨ Principais Funcionalidades

- 🖼️ Compartilhe desenhos únicos ou histórias em quadrinhos
- 💬 Sistema de chat privado com suporte a imagens
- ❤️ Interaja através de curtidas, favoritos e comentários
- 👥 Siga artistas e construa sua rede
- 📱 Interface intuitiva e responsiva

![image](https://github.com/user-attachments/assets/e5f25caa-64d9-49cc-941a-327038de0c14)
![image](https://github.com/user-attachments/assets/f7ad537f-24e0-42d7-b824-73fa55020f75)![image](https://github.com/user-attachments/assets/de7b5d2a-b47e-41ae-8952-f009cb7b1d4c)




## 🚀 Executando o projeto

### Instalando dependências

```
pip install -r requirements.txt
```

### Definindo variáveis de ambiente
As variáveis de ambiente utilizadas no sistema devem ser definidas em um arquivo `.env`.
Estas variáveis devem estar incluídas no arquivo `.env-EXAMPLE` para que outros desenvolvedores saibam o que é necessário.

### Carregando migrações

```
py manage.py migrate
```

### Iniciando o servidor

```
py manage.py runserver
```

## 💻 Sobre o desenvolvimento
Para o desenvolvimento de novas funcionalidades, recomenda-se criar uma branch separada da `main`. 
Além disso, ao invés de fazer merge diretamente na branch `main`, deve-se criar um pull request e solicitar revisão,
garantindo assim a qualidade do código e evitando conflitos.
