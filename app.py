import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import math

# Configuración de la página
st.set_page_config(
    page_title="Planificador Financiero 50-30-20",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .warning-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-left: 5px solid #fdcb6e;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-card {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-left: 5px solid #00b894;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .danger-card {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-left: 5px solid #e17055;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .investment-option {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .investment-option:hover {
        background: #e9ecef;
        border-color: #667eea;
        transform: scale(1.02);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stTab > div > div > div > div {
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Clases para el manejo de datos
class FinancialPlanner:
    def __init__(self):
        self.income = 0
        self.needs = {}
        self.wants = {}
        self.savings_investments = 0
        self.family_info = {}
        
    def calculate_percentages(self):
        return {
            'needs_budget': self.income * 0.50,
            'wants_budget': self.income * 0.30,
            'savings_budget': self.income * 0.20
        }
    
    def calculate_needs_total(self):
        return sum(self.needs.values())
    
    def calculate_wants_total(self):
        return sum(self.wants.values())
    
    def get_risk_analysis(self):
        budgets = self.calculate_percentages()
        needs_total = self.calculate_needs_total()
        
        risk_level = "Bajo"
        risk_color = "#00b894"
        recommendations = []
        
        if needs_total > budgets['needs_budget']:
            excess = needs_total - budgets['needs_budget']
            excess_percent = (excess / self.income) * 100
            
            if excess_percent > 20:
                risk_level = "Alto"
                risk_color = "#e17055"
                recommendations.extend([
                    "🚨 Urgente: Reducir gastos básicos o aumentar ingresos",
                    "📊 Revisar todos los gastos y eliminar los no esenciales",
                    "💼 Considerar fuentes de ingresos adicionales"
                ])
            elif excess_percent > 10:
                risk_level = "Medio"
                risk_color = "#fdcb6e"
                recommendations.extend([
                    "⚠️ Advertencia: Gastos básicos exceden el presupuesto",
                    "🔍 Identificar gastos reducibles",
                    "📈 Planificar aumento de ingresos"
                ])
        else:
            recommendations.extend([
                "✅ Gastos básicos bajo control",
                "💡 Considerar optimizar aún más para aumentar ahorros",
                "🎯 Mantener disciplina financiera"
            ])
        
        return {
            'level': risk_level,
            'color': risk_color,
            'recommendations': recommendations,
            'needs_excess': max(0, needs_total - budgets['needs_budget'])
        }

class InvestmentAdvisor:
    @staticmethod
    def get_investment_options(amount):
        options = []
        
        if amount >= 50000:  # Monto alto
            options.extend([
                {
                    'name': 'CDT a Largo Plazo',
                    'risk': 'Bajo',
                    'return': '8-12%',
                    'description': 'Certificados de depósito a término con excelente rentabilidad',
                    'min_amount': 50000,
                    'liquidity': 'Baja'
                },
                {
                    'name': 'Fondos de Inversión Diversificados',
                    'risk': 'Medio',
                    'return': '12-18%',
                    'description': 'Portafolio diversificado gestionado profesionalmente',
                    'min_amount': 50000,
                    'liquidity': 'Media'
                },
                {
                    'name': 'Acciones Blue Chip',
                    'risk': 'Medio-Alto',
                    'return': '15-25%',
                    'description': 'Acciones de empresas establecidas con dividendos',
                    'min_amount': 100000,
                    'liquidity': 'Alta'
                }
            ])
        
        if amount >= 20000:  # Monto medio
            options.extend([
                {
                    'name': 'Fondos Mutuos',
                    'risk': 'Medio',
                    'return': '10-15%',
                    'description': 'Inversión colectiva con diversificación automática',
                    'min_amount': 20000,
                    'liquidity': 'Media'
                },
                {
                    'name': 'CDT a Mediano Plazo',
                    'risk': 'Bajo',
                    'return': '6-10%',
                    'description': 'Inversión segura con rentabilidad fija',
                    'min_amount': 20000,
                    'liquidity': 'Baja'
                }
            ])
        
        if amount >= 5000:  # Monto básico
            options.extend([
                {
                    'name': 'Cuenta de Ahorros Premium',
                    'risk': 'Muy Bajo',
                    'return': '4-6%',
                    'description': 'Alta liquidez con mejor rentabilidad que cuentas tradicionales',
                    'min_amount': 5000,
                    'liquidity': 'Alta'
                },
                {
                    'name': 'Fondos de Renta Fija',
                    'risk': 'Bajo',
                    'return': '6-9%',
                    'description': 'Inversión conservadora en bonos y títulos de deuda',
                    'min_amount': 10000,
                    'liquidity': 'Media'
                }
            ])
        
        # Opciones para montos pequeños
        if amount < 20000:
            options.extend([
                {
                    'name': 'Micro-inversiones',
                    'risk': 'Medio',
                    'return': '8-15%',
                    'description': 'Plataformas digitales para pequeños inversionistas',
                    'min_amount': 1000,
                    'liquidity': 'Alta'
                },
                {
                    'name': 'Educación Financiera',
                    'risk': 'Nulo',
                    'return': 'Invaluable',
                    'description': 'Inversión en conocimiento para mejores decisiones futuras',
                    'min_amount': 0,
                    'liquidity': 'Inmediata'
                }
            ])
        
        return options

# Función principal de la aplicación
def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>💰 Planificador Financiero Inteligente</h1>
        <p>Basado en el Modelo 50-30-20 | Análisis de Riesgo Personalizado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar session state
    if 'planner' not in st.session_state:
        st.session_state.planner = FinancialPlanner()
    
    planner = st.session_state.planner
    
    # Sidebar para información personal
    with st.sidebar:
        st.header("📋 Información Personal")
        
        # Información básica
        st.subheader("💼 Ingresos")
        planner.income = st.number_input(
            "Salario mensual neto (COP)",
            min_value=0,
            value=planner.income,
            step=50000,
            format="%d",
            help="Ingrese su salario mensual después de impuestos"
        )
        
        # Información familiar
        st.subheader("👨‍👩‍👧‍👦 Composición Familiar")
        planner.family_info['has_children'] = st.checkbox("¿Tiene hijos?", value=planner.family_info.get('has_children', False))
        
        if planner.family_info['has_children']:
            planner.family_info['num_children'] = st.number_input(
                "Número de hijos",
                min_value=1,
                max_value=10,
                value=planner.family_info.get('num_children', 1)
            )
            planner.family_info['children_ages'] = st.text_input(
                "Edades de los hijos (separadas por comas)",
                value=planner.family_info.get('children_ages', ""),
                help="Ejemplo: 5, 8, 12"
            )
        
        planner.family_info['has_pets'] = st.checkbox("¿Tiene mascotas?", value=planner.family_info.get('has_pets', False))
        
        if planner.family_info['has_pets']:
            planner.family_info['num_pets'] = st.number_input(
                "Número de mascotas",
                min_value=1,
                max_value=5,
                value=planner.family_info.get('num_pets', 1)
            )
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Necesidades (50%)",
        "🎯 Deseos (30%)",
        "💰 Ahorros e Inversiones (20%)",
        "📊 Análisis Completo",
        "📈 Plan de Compras"
    ])
    
    with tab1:
        st.header("🏠 Gastos Básicos y Necesidades (50% del Salario)")
        
        if planner.income > 0:
            budgets = planner.calculate_percentages()
            st.info(f"💡 **Presupuesto disponible para necesidades:** ${budgets['needs_budget']:,.0f} COP")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏘️ Vivienda")
                planner.needs['rent'] = st.number_input(
                    "Arriendo/Hipoteca", 
                    min_value=0, 
                    value=planner.needs.get('rent', 0),
                    step=50000
                )
                planner.needs['utilities'] = st.number_input(
                    "Servicios públicos", 
                    min_value=0, 
                    value=planner.needs.get('utilities', 0),
                    step=10000
                )
                
                st.subheader("🍽️ Alimentación")
                planner.needs['groceries'] = st.number_input(
                    "Mercado/Comida", 
                    min_value=0, 
                    value=planner.needs.get('groceries', 0),
                    step=50000
                )
                
                st.subheader("🚗 Transporte")
                planner.needs['transport'] = st.number_input(
                    "Transporte público/Combustible", 
                    min_value=0, 
                    value=planner.needs.get('transport', 0),
                    step=25000
                )
            
            with col2:
                st.subheader("🏥 Salud")
                planner.needs['health'] = st.number_input(
                    "Medicina prepagada/Seguros", 
                    min_value=0, 
                    value=planner.needs.get('health', 0),
                    step=25000
                )
                
                if planner.family_info.get('has_children'):
                    st.subheader("👶 Gastos de Hijos")
                    planner.needs['children'] = st.number_input(
                        "Educación/Cuidado de niños", 
                        min_value=0, 
                        value=planner.needs.get('children', 0),
                        step=50000
                    )
                
                if planner.family_info.get('has_pets'):
                    st.subheader("🐕 Gastos de Mascotas")
                    planner.needs['pets'] = st.number_input(
                        "Comida/Veterinario mascotas", 
                        min_value=0, 
                        value=planner.needs.get('pets', 0),
                        step=25000
                    )
                
                st.subheader("📱 Otros Básicos")
                planner.needs['phone'] = st.number_input(
                    "Teléfono/Internet", 
                    min_value=0, 
                    value=planner.needs.get('phone', 0),
                    step=25000
                )
            
            # Análisis de necesidades
            total_needs = planner.calculate_needs_total()
            if total_needs > budgets['needs_budget']:
                excess = total_needs - budgets['needs_budget']
                excess_percent = (excess / planner.income) * 100
                st.markdown(f"""
                <div class="danger-card">
                    <h4>⚠️ ALERTA: Exceso en Gastos Básicos</h4>
                    <p><strong>Total gastado:</strong> ${total_needs:,.0f} COP</p>
                    <p><strong>Presupuesto:</strong> ${budgets['needs_budget']:,.0f} COP</p>
                    <p><strong>Exceso:</strong> ${excess:,.0f} COP ({excess_percent:.1f}% del salario)</p>
                    <p><strong>Recomendación:</strong> Debe reducir gastos básicos o aumentar ingresos urgentemente.</p>
                </div>
                """, unsafe_allow_html=True)
            elif total_needs > budgets['needs_budget'] * 0.9:
                st.markdown(f"""
                <div class="warning-card">
                    <h4>⚡ Advertencia: Cerca del Límite</h4>
                    <p><strong>Total gastado:</strong> ${total_needs:,.0f} COP</p>
                    <p><strong>Presupuesto:</strong> ${budgets['needs_budget']:,.0f} COP</p>
                    <p><strong>Margen restante:</strong> ${budgets['needs_budget'] - total_needs:,.0f} COP</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                remaining = budgets['needs_budget'] - total_needs
                st.markdown(f"""
                <div class="success-card">
                    <h4>✅ Gastos Básicos Bajo Control</h4>
                    <p><strong>Total gastado:</strong> ${total_needs:,.0f} COP</p>
                    <p><strong>Presupuesto:</strong> ${budgets['needs_budget']:,.0f} COP</p>
                    <p><strong>Disponible:</strong> ${remaining:,.0f} COP</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Por favor, ingrese su salario mensual en la barra lateral para continuar.")
    
    with tab2:
        st.header("🎯 Deseos y Gustos Personales (30% del Salario)")
        
        if planner.income > 0:
            budgets = planner.calculate_percentages()
            st.info(f"💡 **Presupuesto disponible para deseos:** ${budgets['wants_budget']:,.0f} COP")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎬 Entretenimiento")
                planner.wants['entertainment'] = st.number_input(
                    "Cine, streaming, salidas", 
                    min_value=0, 
                    value=planner.wants.get('entertainment', 0),
                    step=25000
                )
                
                st.subheader("🍽️ Restaurantes")
                planner.wants['dining'] = st.number_input(
                    "Restaurantes y delivery", 
                    min_value=0, 
                    value=planner.wants.get('dining', 0),
                    step=25000
                )
                
                st.subheader("👕 Ropa y Accesorios")
                planner.wants['clothing'] = st.number_input(
                    "Ropa no esencial", 
                    min_value=0, 
                    value=planner.wants.get('clothing', 0),
                    step=50000
                )
            
            with col2:
                st.subheader("🎮 Hobbies")
                planner.wants['hobbies'] = st.number_input(
                    "Videojuegos, deportes, aficiones", 
                    min_value=0, 
                    value=planner.wants.get('hobbies', 0),
                    step=25000
                )
                
                st.subheader("✈️ Viajes")
                planner.wants['travel'] = st.number_input(
                    "Vacaciones y viajes", 
                    min_value=0, 
                    value=planner.wants.get('travel', 0),
                    step=100000
                )
                
                st.subheader("🛍️ Compras Impulsivas")
                planner.wants['shopping'] = st.number_input(
                    "Compras no planificadas", 
                    min_value=0, 
                    value=planner.wants.get('shopping', 0),
                    step=25000
                )
            
            total_wants = planner.calculate_wants_total()
            
            if total_wants > budgets['wants_budget']:
                excess = total_wants - budgets['wants_budget']
                st.markdown(f"""
                <div class="warning-card">
                    <h4>💸 Exceso en Gastos de Deseos</h4>
                    <p><strong>Total en deseos:</strong> ${total_wants:,.0f} COP</p>
                    <p><strong>Presupuesto:</strong> ${budgets['wants_budget']:,.0f} COP</p>
                    <p><strong>Exceso:</strong> ${excess:,.0f} COP</p>
                    <p>💡 <strong>Sugerencia:</strong> Priorice sus deseos y reduzca gastos no esenciales.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                remaining = budgets['wants_budget'] - total_wants
                st.markdown(f"""
                <div class="success-card">
                    <h4>🎉 Presupuesto de Deseos Controlado</h4>
                    <p><strong>Total gastado:</strong> ${total_wants:,.0f} COP</p>
                    <p><strong>Disponible:</strong> ${remaining:,.0f} COP para otros gustos</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Por favor, ingrese su salario mensual en la barra lateral.")
    
    with tab3:
        st.header("💰 Ahorros e Inversiones (20% del Salario)")
        
        if planner.income > 0:
            budgets = planner.calculate_percentages()
            st.info(f"💡 **Presupuesto obligatorio para ahorros:** ${budgets['savings_budget']:,.0f} COP")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🆘 Fondo de Emergencia")
                emergency_fund = st.number_input(
                    "Fondo de emergencia mensual", 
                    min_value=0, 
                    value=budgets['savings_budget'] * 0.6,
                    step=25000,
                    help="Recomendado: 60% de este presupuesto"
                )
                
                months_expenses = planner.calculate_needs_total()
                if months_expenses > 0:
                    recommended_emergency = months_expenses * 6
                    st.info(f"💡 **Fondo de emergencia recomendado:** ${recommended_emergency:,.0f} COP (6 meses de gastos básicos)")
            
            with col2:
                st.subheader("📈 Inversiones")
                investment_amount = st.number_input(
                    "Monto mensual para inversiones", 
                    min_value=0, 
                    value=budgets['savings_budget'] * 0.4,
                    step=25000,
                    help="Recomendado: 40% de este presupuesto"
                )
            
            # Análisis de inversiones
            if investment_amount > 0:
                st.subheader("🎯 Recomendaciones de Inversión")
                
                advisor = InvestmentAdvisor()
                investment_options = advisor.get_investment_options(investment_amount * 12)  # Anual
                
                for option in investment_options:
                    with st.expander(f"💼 {option['name']} - Riesgo: {option['risk']}"):
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.metric("Rentabilidad Esperada", option['return'])
                        
                        with col_b:
                            st.metric("Inversión Mínima", f"${option['min_amount']:,.0f}")
                        
                        with col_c:
                            st.metric("Liquidez", option['liquidity'])
                        
                        st.write(option['description'])
                        
                        if investment_amount * 12 >= option['min_amount']:
                            st.success("✅ Su presupuesto es suficiente para esta opción")
                        else:
                            needed = option['min_amount'] - (investment_amount * 12)
                            months_needed = math.ceil(needed / investment_amount)
                            st.warning(f"⏰ Necesita ahorrar {months_needed} meses más para alcanzar la inversión mínima")
            
            # Visualización del progreso
            total_savings = emergency_fund + investment_amount
            if total_savings < budgets['savings_budget']:
                remaining = budgets['savings_budget'] - total_savings
                st.markdown(f"""
                <div class="warning-card">
                    <h4>⚠️ No está cumpliendo con el 20% de ahorro</h4>
                    <p><strong>Ahorrando actualmente:</strong> ${total_savings:,.0f} COP</p>
                    <p><strong>Debería ahorrar:</strong> ${budgets['savings_budget']:,.0f} COP</p>
                    <p><strong>Faltante:</strong> ${remaining:,.0f} COP</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="success-card">
                    <h4>🎯 ¡Excelente! Cumpliendo con el ahorro obligatorio</h4>
                    <p><strong>Ahorro mensual:</strong> ${total_savings:,.0f} COP</p>
                    <p><strong>Ahorro anual proyectado:</strong> ${total_savings * 12:,.0f} COP</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Por favor, ingrese su salario mensual en la barra lateral.")
    
    with tab4:
        st.header("📊 Análisis Financiero Completo")
        
        if planner.income > 0:
            # Cálculos generales
            budgets = planner.calculate_percentages()
            total_needs = planner.calculate_needs_total()
            total_wants = planner.calculate_wants_total()
            risk_analysis = planner.get_risk_analysis()
            
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "💰 Salario Mensual",
                    f"${planner.income:,.0f}",
                    help="Su ingreso mensual neto"
                )
            
            with col2:
                needs_percent = (total_needs / planner.income) * 100 if planner.income > 0 else 0
                delta_needs = needs_percent - 50
                st.metric(
                    "🏠 Gastos Básicos",
                    f"{needs_percent:.1f}%",
                    f"{delta_needs:+.1f}%",
                    delta_color="inverse"
                )
            
            with col3:
                wants_percent = (total_wants / planner.income) * 100 if planner.income > 0 else 0
                delta_wants = wants_percent - 30
                st.metric(
                    "🎯 Deseos",
                    f"{wants_percent:.1f}%",
                    f"{delta_wants:+.1f}%",
                    delta_color="inverse"
                )
            
            with col4:
                st.metric(
                    "⚠️ Nivel de Riesgo",
                    risk_analysis['level'],
                    help="Basado en el análisis de sus gastos"
                )
            
            # Gráfico de distribución
            st.subheader("📈 Distribución de Ingresos")
            
            # Datos para el gráfico
            categories = ['Necesidades\n(50%)', 'Deseos\n(30%)', 'Ahorros\n(20%)', 'Sin Asignar']
            actual_values = [
                total_needs,
                total_wants,
                budgets['savings_budget'],
                max(0, planner.income - total_needs - total_wants - budgets['savings_budget'])
            ]
            
            budget_values = [
                budgets['needs_budget'],
                budgets['wants_budget'],
                budgets['savings_budget'],
                0
            ]
            
            # Crear gráfico de barras comparativo
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Distribución Actual vs Recomendada', 'Análisis por Categorías'),
                specs=[[{"type": "bar"}], [{"type": "pie"}]],
                vertical_spacing=0.12
            )
            
            # Gráfico de barras
            fig.add_trace(
                go.Bar(name='Actual', x=categories[:-1], y=actual_values[:-1], 
                       marker_color=['#e17055', '#fdcb6e', '#00b894']),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(name='Recomendado', x=categories[:-1], y=budget_values[:-1], 
                       marker_color=['#ff7675', '#ffeaa7', '#55a3ff'], opacity=0.7),
                row=1, col=1
            )
            
            # Gráfico circular
            fig.add_trace(
                go.Pie(labels=categories, values=actual_values, 
                       marker_colors=['#e17055', '#fdcb6e', '#00b894', '#ddd']),
                row=2, col=1
            )
            
            fig.update_layout(
                height=800,
                title_text="Análisis Financiero Detallado",
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Recomendaciones personalizadas
            st.subheader("🎯 Recomendaciones Personalizadas")
            
            for i, recommendation in enumerate(risk_analysis['recommendations'], 1):
                st.write(f"{i}. {recommendation}")
            
            # Proyección anual
            st.subheader("📅 Proyección Anual")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                annual_needs = total_needs * 12
                st.metric("Gastos Básicos Anuales", f"${annual_needs:,.0f}")
            
            with col2:
                annual_wants = total_wants * 12
                st.metric("Gastos de Deseos Anuales", f"${annual_wants:,.0f}")
            
            with col3:
                annual_savings = budgets['savings_budget'] * 12
                st.metric("Ahorro Anual Recomendado", f"${annual_savings:,.0f}")
            
            # Análisis de flujo de caja
            st.subheader("💸 Flujo de Caja Mensual")
            
            remaining_income = planner.income - total_needs - total_wants - budgets['savings_budget']
            
            if remaining_income < 0:
                st.markdown(f"""
                <div class="danger-card">
                    <h4>🚨 DÉFICIT FINANCIERO</h4>
                    <p><strong>Déficit mensual:</strong> ${abs(remaining_income):,.0f} COP</p>
                    <p><strong>Acción requerida:</strong> Reducir gastos o aumentar ingresos inmediatamente.</p>
                </div>
                """, unsafe_allow_html=True)
            elif remaining_income < planner.income * 0.05:
                st.markdown(f"""
                <div class="warning-card">
                    <h4>⚠️ MARGEN AJUSTADO</h4>
                    <p><strong>Sobrante mensual:</strong> ${remaining_income:,.0f} COP</p>
                    <p>Margen muy ajustado, considere optimizar gastos.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="success-card">
                    <h4>✅ SITUACIÓN FINANCIERA SALUDABLE</h4>
                    <p><strong>Sobrante mensual:</strong> ${remaining_income:,.0f} COP</p>
                    <p>Puede considerar aumentar ahorros o inversiones.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Complete la información de ingresos y gastos para ver el análisis completo.")
    
    with tab5:
        st.header("📈 Planificador de Compras Importantes")
        
        if planner.income > 0:
            budgets = planner.calculate_percentages()
            available_wants = budgets['wants_budget'] - planner.calculate_wants_total()
            
            st.info(f"💡 **Presupuesto disponible mensual para compras:** ${max(0, available_wants):,.0f} COP")
            
            # Formulario para nueva compra
            st.subheader("🛍️ Nueva Compra Planificada")
            
            col1, col2 = st.columns(2)
            
            with col1:
                item_name = st.text_input("¿Qué desea comprar?", placeholder="Ejemplo: iPhone 15, Laptop, Carro")
                item_price = st.number_input(
                    "Precio del producto (COP)", 
                    min_value=0, 
                    step=100000,
                    format="%d"
                )
            
            with col2:
                priority = st.selectbox(
                    "Prioridad de la compra",
                    ["Alta", "Media", "Baja"]
                )
                
                save_percentage = st.slider(
                    "¿Qué % de su presupuesto de deseos destinará a esta compra?",
                    min_value=10,
                    max_value=100,
                    value=50,
                    step=5
                ) / 100
            
            if item_name and item_price > 0 and available_wants > 0:
                monthly_save = available_wants * save_percentage
                months_needed = math.ceil(item_price / monthly_save) if monthly_save > 0 else float('inf')
                
                # Información de la compra
                st.subheader(f"📊 Plan de Ahorro: {item_name}")
                
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    st.metric("💰 Precio Total", f"${item_price:,.0f}")
                
                with col_b:
                    st.metric("💳 Ahorro Mensual", f"${monthly_save:,.0f}")
                
                with col_c:
                    st.metric("📅 Meses Necesarios", f"{months_needed}")
                
                with col_d:
                    target_date = datetime.now() + timedelta(days=30 * months_needed)
                    st.metric("🎯 Fecha Objetivo", target_date.strftime("%m/%Y"))
                
                # Gráfico de progreso de ahorro
                if months_needed <= 60:  # Solo mostrar si es razonable
                    progress_data = []
                    cumulative = 0
                    
                    for month in range(int(months_needed) + 1):
                        cumulative += monthly_save if month < months_needed else 0
                        progress_data.append({
                            'Mes': month,
                            'Ahorro Acumulado': min(cumulative, item_price),
                            'Meta': item_price
                        })
                    
                    df_progress = pd.DataFrame(progress_data)
                    
                    fig_progress = px.line(
                        df_progress, 
                        x='Mes', 
                        y=['Ahorro Acumulado', 'Meta'],
                        title=f"Progreso de Ahorro para {item_name}",
                        color_discrete_map={
                            'Ahorro Acumulado': '#00b894',
                            'Meta': '#e17055'
                        }
                    )
                    
                    fig_progress.update_layout(
                        xaxis_title="Meses",
                        yaxis_title="Monto (COP)",
                        height=400
                    )
                    
                    st.plotly_chart(fig_progress, use_container_width=True)
                    
                    # Recomendaciones para la compra
                    if months_needed <= 6:
                        st.markdown(f"""
                        <div class="success-card">
                            <h4>🎉 Compra Alcanzable</h4>
                            <p>Podrá comprar <strong>{item_name}</strong> en {months_needed} meses.</p>
                            <p><strong>Estrategia:</strong> Mantenga disciplina en el ahorro mensual.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif months_needed <= 12:
                        st.markdown(f"""
                        <div class="warning-card">
                            <h4>⏰ Compra a Mediano Plazo</h4>
                            <p>Necesitará {months_needed} meses para comprar <strong>{item_name}</strong>.</p>
                            <p><strong>Sugerencias:</strong></p>
                            <ul>
                                <li>Considere aumentar el % destinado al ahorro</li>
                                <li>Busque ofertas o descuentos</li>
                                <li>Evalúe comprar una versión más económica</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="danger-card">
                            <h4>🚨 Compra a Muy Largo Plazo</h4>
                            <p>Necesitará {months_needed} meses para esta compra.</p>
                            <p><strong>Recomendaciones:</strong></p>
                            <ul>
                                <li>Reconsidere si realmente necesita esta compra</li>
                                <li>Aumente significativamente sus ingresos</li>
                                <li>Reduzca otros gastos de deseos</li>
                                <li>Busque alternativas más económicas</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Comparación con financiamiento
                    st.subheader("💳 Comparación: Ahorro vs Financiamiento")
                    
                    # Simulación de crédito (ejemplo con 24% anual)
                    if months_needed > 3:
                        monthly_rate = 0.24 / 12  # 24% anual
                        loan_months = min(months_needed, 36)  # Máximo 36 meses
                        
                        if monthly_rate > 0:
                            monthly_payment = (item_price * monthly_rate * (1 + monthly_rate)**loan_months) / ((1 + monthly_rate)**loan_months - 1)
                            total_interest = (monthly_payment * loan_months) - item_price
                        else:
                            monthly_payment = item_price / loan_months
                            total_interest = 0
                        
                        col_credit1, col_credit2 = st.columns(2)
                        
                        with col_credit1:
                            st.markdown("### 💰 Ahorrando")
                            st.write(f"**Cuota mensual:** ${monthly_save:,.0f}")
                            st.write(f"**Total pagado:** ${item_price:,.0f}")
                            st.write(f"**Intereses:** $0")
                            st.write(f"**Tiempo:** {months_needed} meses")
                        
                        with col_credit2:
                            st.markdown("### 💳 Financiando (24% anual)")
                            st.write(f"**Cuota mensual:** ${monthly_payment:,.0f}")
                            st.write(f"**Total pagado:** ${monthly_payment * loan_months:,.0f}")
                            st.write(f"**Intereses:** ${total_interest:,.0f}")
                            st.write(f"**Tiempo:** {loan_months} meses")
                        
                        if monthly_payment <= available_wants:
                            savings_vs_credit = total_interest
                            st.success(f"💡 **Ahorrando en lugar de financiar, evitará pagar ${savings_vs_credit:,.0f} en intereses.**")
                        else:
                            st.error(f"⚠️ **La cuota del crédito (${monthly_payment:,.0f}) excede su presupuesto disponible.**")
                
                else:
                    st.warning(f"⏰ El tiempo necesario ({months_needed} meses) es muy largo. Considere reducir el precio objetivo o aumentar el ahorro mensual.")
            
            elif available_wants <= 0:
                st.error("❌ No tiene presupuesto disponible para nuevas compras. Primero optimice sus gastos actuales de deseos.")
            
            # Historial de compras planificadas (simulado)
            st.subheader("📋 Mis Compras Planificadas")
            
            # Esto sería idealmente guardado en una base de datos
            sample_purchases = [
                {"Producto": "Laptop Gaming", "Precio": 3500000, "Ahorro Mensual": 350000, "Meses Restantes": 7, "Progreso": 30},
                {"Producto": "Viaje a Europa", "Precio": 8000000, "Ahorro Mensual": 400000, "Meses Restantes": 15, "Progreso": 25},
                {"Producto": "iPhone 15", "Precio": 4500000, "Ahorro Mensual": 450000, "Meses Restantes": 2, "Progreso": 80}
            ]
            
            if st.checkbox("Ver ejemplo de compras planificadas"):
                df_purchases = pd.DataFrame(sample_purchases)
                
                for idx, purchase in df_purchases.iterrows():
                    with st.expander(f"🛍️ {purchase['Producto']} - {purchase['Progreso']}% completado"):
                        col_p1, col_p2, col_p3 = st.columns(3)
                        
                        with col_p1:
                            st.metric("Precio", f"${purchase['Precio']:,.0f}")
                        
                        with col_p2:
                            st.metric("Ahorro Mensual", f"${purchase['Ahorro Mensual']:,.0f}")
                        
                        with col_p3:
                            st.metric("Meses Restantes", purchase['Meses Restantes'])
                        
                        # Barra de progreso
                        progress_bar = st.progress(purchase['Progreso'] / 100)
                        st.write(f"Progreso: {purchase['Progreso']}%")
        else:
            st.warning("⚠️ Complete la información de ingresos para usar el planificador de compras.")
    
    # Footer con información adicional
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <h3>💡 Sobre el Modelo 50-30-20</h3>
        <p>Este modelo de presupuesto fue popularizado por Elizabeth Warren y sugiere:</p>
        <div style="display: flex; justify-content: space-around; margin: 1rem 0;">
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem;">
                <strong>50% Necesidades</strong><br>
                Gastos esenciales para vivir
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem;">
                <strong>30% Deseos</strong><br>
                Entretenimiento y gustos
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem;">
                <strong>20% Ahorro</strong><br>
                Fondo de emergencia e inversiones
            </div>
        </div>
        <p style="font-size: 0.9em; color: #999;">
            Desarrollado con ❤️ para ayudarte a alcanzar tus metas financieras
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()