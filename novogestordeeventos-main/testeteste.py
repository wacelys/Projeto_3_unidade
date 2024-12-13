body {
    font-family: Helvetica, Arial, sans-serif;
    background-color: #f4f4f9;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.register-container {
    background-color: #fff;
    border-radius: 12px;
    padding: 40px 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 600px;
    display: flex;
    flex-direction: column;
}

h2 {
    font-size: 1.8rem;
    text-align: center;
    margin: 0;
    padding: 15px;
    color: #fff;
    background: linear-gradient(to bottom, #000, #333);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-top: 40px;
}

.form-inputs-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.form-inputs {
    display: flex;
    justify-content: space-between;
    gap: 20px;
}

.form-column {
    display: flex;
    flex-direction: column;
    flex: 1;
    gap: 15px;
}

.form-box {
    display: flex;
    flex-direction: column;
}

label {
    font-size: 1rem;
    color: #000;
    margin-bottom: 5px;
}

input, select {
    padding: 10px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    outline: none;
    transition: border-color 0.3s ease;
}

input:focus, select:focus {
    border-color: #007BFF;
}

.form-button {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

button {
    background-color: #333;
    color: #fff;
    font-size: 1rem;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #D3D3D3;
}

.form-footer {
    text-align: center;
    margin-top: 20px;
}

span {
    display: block;
    font-size: 0.9rem;
}

a {
    color: #007BFF;
    text-decoration: none;
    font-weight: bold;
}

a:hover {
    text-decoration: underline;
}


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../static/css/register.css">
    <title>Cadastro</title>
</head>
<body>
    <div class="register-container">
    <h2>Cadastro de Usuário</h2>
    <div class="line"></div>
    <form action="/registernewuser" method="POST">
        <div class="form-inputs-container">
            <div class="form-inputs">
                <div class="form-column">
                    <div class="form-box">
                        <label for="nome">Nome:</label>
                        <input type="text" id="nome" name="nome" required>
                    </div>
                    <div class="form-box">
                        <label for="email">Email:</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-box">
                        <label for="senha">Senha:</label>
                        <input type="password" id="senha" name="senha" required>
                    </div>
                    <div class="form-box">
                        <label for="repetir-senha">Repetir Senha:</label>
                        <input type="password" id="repetir-senha" name="repetir_senha" required>
                    </div>
                </div>
                <div class="form-column">
                    <div class="form-box">
                        <label for="idade">Idade:</label>
                        <input type="number" id="idade" name="idade" required>
                    </div>
                    <div class="form-box">
                        <label for="profissao">Profissão:</label>
                        <input type="text" id="profissao" name="profissao" required>
                    </div>
                    <div class="form-box">
                        <label for="estado">Estado:</label>
                        <select id="estado" name="estado" required>
                            <option value="">Selecione seu estado</option>
                            <option value="AC">Acre</option>
                            <option value="AL">Alagoas</option>
                            <option value="AP">Amapá</option>
                            <option value="AM">Amazonas</option>
                            <option value="BA">Bahia</option>
                            <option value="CE">Ceará</option>
                            <option value="DF">Distrito Federal</option>
                            <option value="ES">Espírito Santo</option>
                            <option value="GO">Goiás</option>
                            <option value="MA">Maranhão</option>
                            <option value="MT">Mato Grosso</option>
                            <option value="MS">Mato Grosso do Sul</option>
                            <option value="MG">Minas Gerais</option>
                            <option value="PA">Pará</option>
                            <option value="PB">Paraíba</option>
                            <option value="PR">Paraná</option>
                            <option value="PE">Pernambuco</option>
                            <option value="PI">Piauí</option>
                            <option value="RJ">Rio de Janeiro</option>
                            <option value="RN">Rio Grande do Norte</option>
                            <option value="RS">Rio Grande do Sul</option>
                            <option value="RO">Rondônia</option>
                            <option value="RR">Roraima</option>
                            <option value="SC">Santa Catarina</option>
                            <option value="SP">São Paulo</option>
                            <option value="SE">Sergipe</option>
                            <option value="TO">Tocantins</option>
                        </select>
                    </div>
                    <div class="form-box">
                        <label for="genero">Gênero:</label>
                        <select id="genero" name="genero" required>
                            <option value="">Selecione seu gênero</option>
                            <option value="masculino">Masculino</option>
                            <option value="feminino">Feminino</option>
                            <option value="outro">Outro</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
        <div class="form-button">
            <button type="submit">Enviar</button>
        </div>
    </form>
    <div class="form-footer">
        <span>Já possui conta? <a href="/">Faça login</a></span>
    </div>
</div>
</body>
</html>

