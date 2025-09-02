import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import math
import calendar

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
    
    .calculation-debug {
        background: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 0.9em;
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
        <h1>💰FinanceFlow-Pro</h1>
        <h2>Planificador Financiero Inteligente</h1>
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

        # === Cálculo del valor hora de trabajo con mes actual ===
        st.header("Valor de tu hora de trabajo")
        
        # Pedimos las horas trabajadas a la semana
        horas_semana = st.number_input(
            "Horas trabajadas por semana", 
            min_value=1, max_value=100, value=44, step=1
        )
        
        # Obtenemos mes y año actual
        hoy = datetime.today()
        mes_actual = hoy.month
        anio_actual = hoy.year
        nombre_mes = calendar.month_name[mes_actual]  # Ej: "August"
        
        # Número de días del mes actual
        dias_mes = calendar.monthrange(anio_actual, mes_actual)[1]
        
        # Semanas reales del mes
        semanas_mes = dias_mes / 7  
        
        # Horas trabajadas al mes según semanas reales
        horas_mes = horas_semana * semanas_mes
        
        # Evitamos división por cero
        if horas_mes > 0 and planner.income > 0:
            valor_hora = planner.income / horas_mes
            st.metric(
                f"💸 Valor por hora ({nombre_mes} {anio_actual})", 
                f"${valor_hora:,.2f}"
            )
        
        # Información Adicional
        st.markdown("*Created by Angel Torres*")

    
    
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
                    value=int(budgets['savings_budget'] * 0.6),
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
                  value=int(budgets['savings_budget'] * 0.4),
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
                    f"{
