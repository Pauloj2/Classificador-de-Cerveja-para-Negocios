<img width="1003" height="565" alt="image" src="https://github.com/user-attachments/assets/23110086-c5f6-457e-9ab8-b8ab490bbcea" />


# 🍺 Beer Analytics – Classificação Inteligente de Cervejas
Sistema Web + Modelo de Machine Learning para Análise de Qualidade
📌 Descrição Geral

O Beer Analytics é um projeto acadêmico que integra Machine Learning e desenvolvimento web para criar um sistema capaz de classificar cervejas como “Boa” ou “Ruim” com base em avaliações sensoriais e características químicas.

O objetivo é demonstrar como a inteligência artificial pode apoiar negócios do setor cervejeiro, oferecendo suporte à tomada de decisão e ao controle de qualidade.

## 🎯 Objetivo do Projeto

O projeto foi desenvolvido com duas entregas principais:

Modelagem em Machine Learning (KNIME)

Sistema Web para classificação em tempo real

O sistema permite que usuários insiram valores normalizados e recebam:

Classificação da cerveja

Probabilidades associadas

Insights de negócio gerados automaticamente

## 🧠 Machine Learning

A modelagem foi realizada no KNIME Analytics Platform, passando por:

Pré-processamento e normalização dos dados

Análise exploratória

Teste e comparação de algoritmos supervisionados

Algoritmos avaliados

Decision Tree

Random Forest

SVM

KNN

MLP

Modelo escolhido

✔ Random Forest — apresentou o melhor desempenho (acurácia e Kappa).

## 📊 Visualizações Incluídas

As seguintes visualizações foram geradas para análise dos padrões da base de dados:

Histograma

Scatter Plot

Pie Chart

Coordenadas Paralelas

Esses gráficos facilitam a compreensão da distribuição das classes e atributos sensoriais.

## 🌐 Sistema Web

A interface web foi criada para demonstrar a aplicação prática do modelo selecionado.

Funcionalidades principais

Ajuste de valores por meio de sliders

Envio dos dados para uma API

Exibição da classificação (“Boa” ou “Ruim”)

Exibição da probabilidade de cada classe

Mensagens estratégicas para o mercado cervejeiro (insights de negócio)

## 💼 Aplicações Reais

O projeto pode ser aplicado como base para:

Controle de qualidade sensorial

Benchmark entre marcas e estilos

Desenvolvimento e ajustes de receitas

Análises estratégicas de mercado

Apoio a decisões de precificação e portfólio

## 🚀 Tecnologias Utilizadas

KNIME Analytics Platform – Pré-processamento, modelagem e avaliação

PMML – Exportação do modelo

Python (API) – Consumo do modelo e predição

HTML, CSS, JavaScript – Interface web

Fetch API – Comunicação entre o front-end e a API

📁 Estrutura do Projeto
📦 Beer-Analytics
 ├── 📂 api/           → API de previsão usando o modelo PMML
 ├── 📂 web/           → Interface web do classificador
 ├── 📂 img/           → Gráficos e visualizações do KNIME
 ├── Modelo.pmml       → Modelo Random Forest exportado
 └── README.md

## 👨‍💻 Autor

Projeto desenvolvido para fins acadêmicos, unindo:

Analise exploratória de dados

Modelagem supervisionada

Desenvolvimento de sistemas web aplicados ao mercado cervejeiro
