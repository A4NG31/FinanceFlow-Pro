import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import math
import calendar
import json
import uuid

# Configuración de la página
st.set_page_config(
    page_title="Planificador Financiero 50-30-20",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado (mismo que antes)
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
    
    .expense-item {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Clases mejoradas
class ExpenseTracker:
    def __init__(self):
        self.daily_expenses = []
    
    def add_expense(self, date, category, subcategory, amount, description=""):
        expense = {
            'id': str(uuid.uuid4()),
            'date': date,
            'category': category,
            'subcategory': subcategory,
            'amount': amount,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
        self.daily_expenses.append(expense)
        return expense['id']
    
    def get_expenses_by_month(self, month, year):
        return [
            expense for expense in self.daily_expenses 
            if expense['date'].month == month and expense['date'].year == year
        ]
    
    def get_category_totals(self, start_date, end_date):
        relevant_expenses = [
            expense for expense in self.daily_expenses
            if start_date <= expense['date'] <= end_date
        ]
        
        totals = {}
        for expense in relevant_expenses:
            category = expense['category']
            if category not in totals:
                totals[category] = {}
            
            subcategory = expense['subcategory']
            if subcategory not in totals[category]:
                totals[category][subcategory] = 0
            
            totals[category][subcategory] += expense['amount']
        
        return totals

class FinancialPlanner:
    def __init__(self):
        self.income = 0
        self.needs = {}
        self.wants = {}
        self.savings_investments = 0
        self.family_info = {}
        self.planned_purchases = []
        self.expense_tracker = ExpenseTracker()
        
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
    
    def add_planned_purchase(self, name, price, priority, save_percentage):
        available_wants = self.calculate_percentages()['wants_budget'] - self.calculate_wants_total()
        max_monthly_save = available_wants * save_percentage
        
        if max_monthly_save > 0:
            months_needed = math.ceil(price / max_monthly_save)
            monthly_save = price / months_needed
            
            purchase = {
                'id': str(uuid.uuid4()),
                'name': name,
                'price': price,
                'priority': priority,
                'monthly_save': monthly_save,
                'months_needed': months_needed,
                'months_completed': 0,
                'amount_saved': 0,
                'created_date': datetime.now().isoformat(),
                'target_date': (datetime.now() + timedelta(days=30 * months_needed)).isoformat()
            }
            
            self.planned_purchases.append(purchase)
            return purchase['id']
        return None
    
    def update_purchase_progress(self, purchase_id, payment_amount):
        for purchase in self.planned_purchases:
            if purchase['id'] == purchase_id:
                purchase['amount_saved'] += payment_amount
                purchase['months_completed'] = purchase['amount_saved'] / purchase['monthly_save']
                break
    
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

class DataManager:
    @staticmethod
    def export_data(planner):
        """Exporta todos los datos del planificador a formato JSON"""
        data = {
            'version': '1.0',
            'export_date': datetime.now().isoformat(),
            'income': planner.income,
            'needs': planner.needs,
            'wants': planner.wants,
            'family_info': planner.family_info,
            'planned_purchases': planner.planned_purchases,
            'daily_expenses': planner.expense_tracker.daily_expenses
        }
        return json.dumps(data, indent=2, default=str)
    
    @staticmethod
    def import_data(json_data):
        """Importa datos desde JSON al planificador"""
        try:
            data = json.loads(json_data)
            
            planner = FinancialPlanner()
            planner.income = data.get('income', 0)
            planner.needs = data.get('needs', {})
            planner.wants = data.get('wants', {})
            planner.family_info = data.get('family_info', {})
            planner.planned_purchases = data.get('planned_purchases', [])
            
            # Reconstruir expense tracker
            planner.expense_tracker = ExpenseTracker()
            for expense in data.get('daily_expenses', []):
                if isinstance(expense['date'], str):
                    expense['date'] = datetime.fromisoformat(expense['date'].replace('Z', '+00:00')).date()
                planner.expense_tracker.daily_expenses.append(expense)
            
            return planner, None
        except Exception as e:
            return None, str(e)

# Función principal mejorada
def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>💰 FinanceFlow-Pro</h1>
        <h2>Planificador Financiero Inteligente</h2>
        <p>Modelo 50-30-20 | Seguimiento en Tiempo Real | Persistencia de Datos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar session state
    if 'planner' not in st.session_state:
        st.session_state.planner = FinancialPlanner()
    
    planner = st.session_state.planner
    
    # Sidebar mejorado
    with st.sidebar:
        st.header("📋 Gestión de Datos")
        
        # Importar/Exportar datos
        with st.expander("💾 Importar/Exportar Datos"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📤 Exportar Datos"):
                    export_data = DataManager.export_data(planner)
                    st.download_button(
                        label="⬇️ Descargar JSON",
                        data=export_data,
                        file_name=f"finanzas_personales_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
            
            with col2:
                uploaded_file = st.file_uploader("📤 Importar Datos", type=['json'])
                if uploaded_file is not None:
                    try:
                        json_data = uploaded_file.read().decode('utf-8')
                        imported_planner, error = DataManager.import_data(json_data)
                        
                        if error:
                            st.error(f"Error al importar: {error}")
                        else:
                            st.session_state.planner = imported_planner
                            st.success("✅ Datos importados correctamente")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error al leer el archivo: {str(e)}")
        
        # Información básica
        st.header("💼 Información Personal")
        
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
        
        planner.family_info['has_pets'] = st.checkbox("¿Tiene mascotas?", value=planner.family_info.get('has_pets', False))
        
        # Valor hora de trabajo
        st.subheader("💸 Valor de tu hora")
        horas_semana = st.number_input(
            "Horas trabajadas por semana", 
            min_value=1, max_value=100, value=44, step=1
        )
        
        if planner.income > 0:
            hoy = datetime.today()
            dias_mes = calendar.monthrange(hoy.year, hoy.month)[1]
            semanas_mes = dias_mes / 7
            horas_mes = horas_semana * semanas_mes
            valor_hora = planner.income / horas_mes
            st.metric(f"💸 Valor por hora", f"${valor_hora:,.0f}")
        
        st.markdown("*Created by Angel Torres*")
    
    # Tabs principales expandidos
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Presupuesto",
        "📝 Gastos Diarios", 
        "📊 Seguimiento",
        "📈 Plan de Compras",
        "📉 Análisis Completo",
        "⚙️ Configuración"
    ])
    
    with tab1:
        st.header("🏠 Configuración de Presupuesto Mensual")
        
        if planner.income > 0:
            budgets = planner.calculate_percentages()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏘️ Necesidades (50%)")
                st.info(f"Presupuesto: ${budgets['needs_budget']:,.0f} COP")
                
                planner.needs['rent'] = st.number_input("Arriendo/Hipoteca", min_value=0, value=planner.needs.get('rent', 0), step=50000)
                planner.needs['utilities'] = st.number_input("Servicios públicos", min_value=0, value=planner.needs.get('utilities', 0), step=10000)
                planner.needs['groceries'] = st.number_input("Mercado/Comida", min_value=0, value=planner.needs.get('groceries', 0), step=50000)
                planner.needs['transport'] = st.number_input("Transporte", min_value=0, value=planner.needs.get('transport', 0), step=25000)
                planner.needs['health'] = st.number_input("Salud/Seguros", min_value=0, value=planner.needs.get('health', 0), step=25000)
                planner.needs['phone'] = st.number_input("Teléfono/Internet", min_value=0, value=planner.needs.get('phone', 0), step=25000)
                
                if planner.family_info.get('has_children'):
                    planner.needs['children'] = st.number_input("Gastos de hijos", min_value=0, value=planner.needs.get('children', 0), step=50000)
                
                if planner.family_info.get('has_pets'):
                    planner.needs['pets'] = st.number_input("Gastos de mascotas", min_value=0, value=planner.needs.get('pets', 0), step=25000)
            
            with col2:
                st.subheader("🎯 Deseos (30%)")
                st.info(f"Presupuesto: ${budgets['wants_budget']:,.0f} COP")
                
                planner.wants['entertainment'] = st.number_input("Entretenimiento", min_value=0, value=planner.wants.get('entertainment', 0), step=25000)
                planner.wants['dining'] = st.number_input("Restaurantes", min_value=0, value=planner.wants.get('dining', 0), step=25000)
                planner.wants['clothing'] = st.number_input("Ropa no esencial", min_value=0, value=planner.wants.get('clothing', 0), step=25000)
                planner.wants['hobbies'] = st.number_input("Hobbies", min_value=0, value=planner.wants.get('hobbies', 0), step=25000)
                planner.wants['travel'] = st.number_input("Viajes", min_value=0, value=planner.wants.get('travel', 0), step=50000)
                planner.wants['shopping'] = st.number_input("Compras impulsivas", min_value=0, value=planner.wants.get('shopping', 0), step=25000)
                
                st.subheader("💰 Ahorros (20%)")
                st.info(f"Presupuesto: ${budgets['savings_budget']:,.0f} COP")
                st.write("Este monto debe destinarse a fondo de emergencia e inversiones")
        else:
            st.warning("⚠️ Configure su salario mensual en la barra lateral")
    
    with tab2:
        st.header("📝 Registro de Gastos Diarios")
        
        if planner.income == 0:
            st.warning("⚠️ Configure primero su presupuesto en la pestaña anterior")
            return
        
        # Formulario para nuevo gasto
        with st.form("new_expense_form"):
            st.subheader("➕ Registrar Nuevo Gasto")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                expense_date = st.date_input(
                    "Fecha del gasto",
                    value=datetime.now().date(),
                    max_value=datetime.now().date()
                )
                
                expense_category = st.selectbox(
                    "Categoría",
                    ["Necesidades", "Deseos", "Ahorros"]
                )
            
            with col2:
                # Subcategorías dinámicas basadas en la categoría
                if expense_category == "Necesidades":
                    subcategories = ["Arriendo/Hipoteca", "Servicios públicos", "Mercado/Comida", 
                                   "Transporte", "Salud/Seguros", "Teléfono/Internet", "Hijos", "Mascotas", "Otros"]
                elif expense_category == "Deseos":
                    subcategories = ["Entretenimiento", "Restaurantes", "Ropa", "Hobbies", "Viajes", "Compras impulsivas", "Otros"]
                else:
                    subcategories = ["Fondo de emergencia", "Inversiones", "Compra planificada", "Otros"]
                
                expense_subcategory = st.selectbox("Subcategoría", subcategories)
                
                expense_amount = st.number_input(
                    "Monto (COP)",
                    min_value=0,
                    step=1000,
                    format="%d"
                )
            
            with col3:
                expense_description = st.text_area(
                    "Descripción (opcional)",
                    max_chars=200,
                    height=100,
                    placeholder="Ej: Supermercado Éxito, Gasolina, etc."
                )
                
                # Opción de vincular a compra planificada
                if expense_category == "Ahorros" and expense_subcategory == "Compra planificada":
                    active_purchases = [p for p in planner.planned_purchases if p['amount_saved'] < p['price']]
                    if active_purchases:
                        purchase_options = ["Seleccionar..."] + [f"{p['name']} (${p['price']:,.0f})" for p in active_purchases]
                        selected_purchase = st.selectbox("Vincular a compra planificada", purchase_options)
            
            submitted = st.form_submit_button("💾 Registrar Gasto", use_container_width=True)
            
            if submitted and expense_amount > 0:
                expense_id = planner.expense_tracker.add_expense(
                    expense_date, expense_category, expense_subcategory, 
                    expense_amount, expense_description
                )
                
                # Si es para una compra planificada, actualizar progreso
                if (expense_category == "Ahorros" and expense_subcategory == "Compra planificada" 
                    and 'selected_purchase' in locals() and selected_purchase != "Seleccionar..."):
                    purchase_name = selected_purchase.split(" (")[0]
                    for purchase in planner.planned_purchases:
                        if purchase['name'] == purchase_name:
                            planner.update_purchase_progress(purchase['id'], expense_amount)
                            break
                
                st.success(f"✅ Gasto registrado: ${expense_amount:,.0f} en {expense_subcategory}")
                st.rerun()
        
        # Gastos recientes
        st.subheader("📋 Gastos Recientes")
        
        if planner.expense_tracker.daily_expenses:
            # Mostrar últimos 10 gastos
            recent_expenses = sorted(
                planner.expense_tracker.daily_expenses, 
                key=lambda x: x['timestamp'], 
                reverse=True
            )[:10]
            
            for expense in recent_expenses:
                with st.expander(f"${expense['amount']:,.0f} - {expense['subcategory']} ({expense['date']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Categoría:** {expense['category']}")
                        st.write(f"**Subcategoría:** {expense['subcategory']}")
                    
                    with col2:
                        st.write(f"**Monto:** ${expense['amount']:,.0f}")
                        st.write(f"**Fecha:** {expense['date']}")
                    
                    with col3:
                        if expense['description']:
                            st.write(f"**Descripción:** {expense['description']}")
                        
                        if st.button(f"🗑️ Eliminar", key=f"del_{expense['id']}"):
                            planner.expense_tracker.daily_expenses = [
                                e for e in planner.expense_tracker.daily_expenses 
                                if e['id'] != expense['id']
                            ]
                            st.rerun()
        else:
            st.info("📝 No hay gastos registrados aún. Comience registrando sus gastos diarios.")
    
    with tab3:
        st.header("📊 Seguimiento vs Presupuesto")
        
        if planner.income == 0:
            st.warning("⚠️ Configure su presupuesto primero")
            return
        
        # Selector de período
        col1, col2 = st.columns(2)
        with col1:
            selected_month = st.selectbox(
                "Mes",
                range(1, 13),
                index=datetime.now().month - 1,
                format_func=lambda x: calendar.month_name[x]
            )
        
        with col2:
            selected_year = st.selectbox(
                "Año",
                range(2020, 2030),
                index=2025 - 2020
            )
        
        # Obtener gastos del período seleccionado
        start_date = datetime(selected_year, selected_month, 1).date()
        end_date = datetime(selected_year, selected_month, calendar.monthrange(selected_year, selected_month)[1]).date()
        
        category_totals = planner.expense_tracker.get_category_totals(start_date, end_date)
        budgets = planner.calculate_percentages()
        
        # Totales por categoría principal
        actual_needs = sum(category_totals.get('Necesidades', {}).values())
        actual_wants = sum(category_totals.get('Deseos', {}).values())
        actual_savings = sum(category_totals.get('Ahorros', {}).values())
        
        # Métricas de seguimiento
        st.subheader(f"📈 Resumen {calendar.month_name[selected_month]} {selected_year}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            needs_percent = (actual_needs / budgets['needs_budget']) * 100 if budgets['needs_budget'] > 0 else 0
            st.metric(
                "🏠 Necesidades",
                f"${actual_needs:,.0f}",
                f"{needs_percent:.1f}% del presupuesto",
                delta_color="inverse" if needs_percent > 100 else "normal"
            )
        
        with col2:
            wants_percent = (actual_wants / budgets['wants_budget']) * 100 if budgets['wants_budget'] > 0 else 0
            st.metric(
                "🎯 Deseos",
                f"${actual_wants:,.0f}",
                f"{wants_percent:.1f}% del presupuesto",
                delta_color="inverse" if wants_percent > 100 else "normal"
            )
        
        with col3:
            savings_percent = (actual_savings / budgets['savings_budget']) * 100 if budgets['savings_budget'] > 0 else 0
            st.metric(
                "💰 Ahorros",
                f"${actual_savings:,.0f}",
                f"{savings_percent:.1f}% del objetivo",
                delta_color="normal" if savings_percent >= 100 else "inverse"
            )
        
        # Gráfico de comparación
        if any(category_totals.values()):
            comparison_data = {
                'Categoría': ['Necesidades', 'Deseos', 'Ahorros'],
                'Presupuestado': [budgets['needs_budget'], budgets['wants_budget'], budgets['savings_budget']],
                'Gastado Real': [actual_needs, actual_wants, actual_savings]
            }
            
            df_comparison = pd.DataFrame(comparison_data)
            
            fig_comparison = px.bar(
                df_comparison,
                x='Categoría',
                y=['Presupuestado', 'Gastado Real'],
                title="Presupuesto vs Gasto Real",
                barmode='group',
                color_discrete_map={
                    'Presupuestado': '#667eea',
                    'Gastado Real': '#00b894'
                }
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Desglose detallado por subcategorías
            st.subheader("🔍 Desglose Detallado por Subcategorías")
            
            for main_category, subcategories in category_totals.items():
                if subcategories:
                    st.write(f"**{main_category}:**")
                    
                    subcategory_df = pd.DataFrame([
                        {'Subcategoría': subcat, 'Monto': amount}
                        for subcat, amount in subcategories.items()
                    ])
                    
                    fig_subcat = px.pie(
                        subcategory_df,
                        values='Monto',
                        names='Subcategoría',
                        title=f"Distribución de {main_category}"
                    )
                    
                    st.plotly_chart(fig_subcat, use_container_width=True)
        else:
            st.info(f"📝 No hay gastos registrados para {calendar.month_name[selected_month]} {selected_year}")
    
    with tab4:
        st.header("📈 Planificador de Compras Importantes")
        
        if planner.income == 0:
            st.warning("⚠️ Configure su presupuesto primero")
            return
        
        budgets = planner.calculate_percentages()
        available_wants = budgets['wants_budget'] - planner.calculate_wants_total()
        
        st.info(f"💡 **Presupuesto disponible mensual:** ${max(0, available_wants):,.0f} COP")
        
        # Formulario para nueva compra planificada
        with st.form("new_purchase_form"):
            st.subheader("🛍️ Nueva Compra Planificada")
            
            col1, col2 = st.columns(2)
            
            with col1:
                item_name = st.text_input("¿Qué desea comprar?", placeholder="Ejemplo: iPhone 15, Laptop")
                item_price = st.number_input("Precio (COP)", min_value=0, step=100000, format="%d")
            
            with col2:
                priority = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])
                save_percentage = st.slider("% del presupuesto disponible", min_value=10, max_value=100, value=50, step=5) / 100
            
            if st.form_submit_button("💾 Agregar a Plan de Compras"):
                if item_name and item_price > 0 and available_wants > 0:
                    purchase_id = planner.add_planned_purchase(item_name, item_price, priority, save_percentage)
                    if purchase_id:
                        st.success(f"✅ {item_name} agregado al plan de compras")
                        st.rerun()
                    else:
                        st.error("❌ No hay presupuesto suficiente")
                else:
                    st.error("❌ Complete todos los campos correctamente")
        
        # Mostrar compras planificadas activas
        st.subheader("🎯 Compras Planificadas Activas")
        
        active_purchases = [p for p in planner.planned_purchases if p['amount_saved'] < p['price']]
        
        if active_purchases:
            for purchase in active_purchases:
                progress_percent = (purchase['amount_saved'] / purchase['price']) * 100
                remaining_amount = purchase['price'] - purchase['amount_saved']
                remaining_months = math.ceil(remaining_amount / purchase['monthly_save']) if purchase['monthly_save'] > 0 else 0
                
                with st.expander(f"🛍️ {purchase['name']} - {progress_percent:.1f}% completado"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("💰 Precio Total", f"${purchase['price']:,.0f}")
                    
                    with col2:
                        st.metric("💳 Ahorrado", f"${purchase['amount_saved']:,.0f}")
                    
                    with col3:
                        st.metric("⏰ Meses Restantes", remaining_months)
                    
                    with col4:
                        st.metric("🎯 Prioridad", purchase['priority'])
                    
                    # Barra de progreso
                    st.progress(progress_percent / 100)
                    
                    # Botones de acción
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        if st.button(f"💰 Registrar Pago", key=f"pay_{purchase['id']}"):
                            st.session_state[f"show_payment_{purchase['id']}"] = True
                    
                    with col_b:
                        if st.button(f"🗑️ Eliminar Meta", key=f"remove_{purchase['id']}"):
                            planner.planned_purchases = [p for p in planner.planned_purchases if p['id'] != purchase['id']]
                            st.rerun()
                    
                    # Formulario de pago rápido
                    if st.session_state.get(f"show_payment_{purchase['id']}", False):
                        with st.form(f"payment_form_{purchase['id']}"):
                            payment_amount = st.number_input(
                                "Monto del pago",
                                min_value=0,
                                max_value=remaining_amount,
                                value=int(purchase['monthly_save']),
                                step=10000
                            )
                            
                            col_pay1, col_pay2 = st.columns(2)
                            
                            with col_pay1:
                                if st.form_submit_button("✅ Confirmar Pago"):
                                    planner.update_purchase_progress(purchase['id'], payment_amount)
                                    planner.expense_tracker.add_expense(
                                        datetime.now().date(),
                                        "Ahorros",
                                        "Compra planificada",
                                        payment_amount,
                                        f"Pago para {purchase['name']}"
                                    )
                                    st.session_state[f"show_payment_{purchase['id']}"] = False
                                    st.rerun()
                            
                            with col_pay2:
                                if st.form_submit_button("❌ Cancelar"):
                                    st.session_state[f"show_payment_{purchase['id']}"] = False
                                    st.rerun()
        else:
            st.info("🎯 No hay compras planificadas. Agregue una en el formulario anterior.")
        
        # Compras completadas
        completed_purchases = [p for p in planner.planned_purchases if p['amount_saved'] >= p['price']]
        
        if completed_purchases:
            st.subheader("🎉 Compras Completadas")
            
            for purchase in completed_purchases:
                completion_date = datetime.fromisoformat(purchase['created_date']) + timedelta(days=30 * purchase['months_completed'])
                
                st.markdown(f"""
                <div class="success-card">
                    <h4>✅ {purchase['name']}</h4>
                    <p><strong>Precio:</strong> ${purchase['price']:,.0f} COP</p>
                    <p><strong>Completado en:</strong> {purchase['months_completed']:.1f} meses</p>
                    <p><strong>Fecha estimada de compra:</strong> {completion_date.strftime('%B %Y')}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab5:
        st.header("📉 Análisis Financiero Completo")
        
        if planner.income == 0:
            st.warning("⚠️ Configure su presupuesto primero")
            return
        
        # Análisis de riesgo mejorado
        budgets = planner.calculate_percentages()
        total_needs = planner.calculate_needs_total()
        total_wants = planner.calculate_wants_total()
        risk_analysis = planner.get_risk_analysis()
        
        # Análisis de gastos reales vs presupuesto
        current_month = datetime.now().month
        current_year = datetime.now().year
        start_date = datetime(current_year, current_month, 1).date()
        end_date = datetime.now().date()
        
        real_expenses = planner.expense_tracker.get_category_totals(start_date, end_date)
        actual_needs_month = sum(real_expenses.get('Necesidades', {}).values())
        actual_wants_month = sum(real_expenses.get('Deseos', {}).values())
        actual_savings_month = sum(real_expenses.get('Ahorros', {}).values())
        
        # Dashboard de métricas
        st.subheader("🎯 Dashboard Financiero")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Salario Mensual", f"${planner.income:,.0f}")
        
        with col2:
            needs_deviation = actual_needs_month - budgets['needs_budget']
            st.metric(
                "🏠 Necesidades",
                f"${actual_needs_month:,.0f}",
                f"{needs_deviation:+,.0f}",
                delta_color="inverse" if needs_deviation > 0 else "normal"
            )
        
        with col3:
            wants_deviation = actual_wants_month - budgets['wants_budget']
            st.metric(
                "🎯 Deseos",
                f"${actual_wants_month:,.0f}",
                f"{wants_deviation:+,.0f}",
                delta_color="inverse" if wants_deviation > 0 else "normal"
            )
        
        with col4:
            savings_deviation = actual_savings_month - budgets['savings_budget']
            st.metric(
                "💰 Ahorros",
                f"${actual_savings_month:,.0f}",
                f"{savings_deviation:+,.0f}",
                delta_color="normal" if savings_deviation >= 0 else "inverse"
            )
        
        # Tendencias mensuales
        if len(planner.expense_tracker.daily_expenses) > 0:
            st.subheader("📈 Tendencias de Gastos")
            
            # Agrupar gastos por mes
            monthly_trends = {}
            for expense in planner.expense_tracker.daily_expenses:
                month_key = f"{expense['date'].year}-{expense['date'].month:02d}"
                if month_key not in monthly_trends:
                    monthly_trends[month_key] = {'Necesidades': 0, 'Deseos': 0, 'Ahorros': 0}
                monthly_trends[month_key][expense['category']] += expense['amount']
            
            if monthly_trends:
                trend_df = pd.DataFrame([
                    {
                        'Mes': month,
                        'Necesidades': data['Necesidades'],
                        'Deseos': data['Deseos'],
                        'Ahorros': data['Ahorros']
                    }
                    for month, data in sorted(monthly_trends.items())
                ])
                
                fig_trends = px.line(
                    trend_df,
                    x='Mes',
                    y=['Necesidades', 'Deseos', 'Ahorros'],
                    title="Tendencia de Gastos por Categoría",
                    color_discrete_map={
                        'Necesidades': '#e17055',
                        'Deseos': '#fdcb6e',
                        'Ahorros': '#00b894'
                    }
                )
                
                st.plotly_chart(fig_trends, use_container_width=True)
        
        # Proyección de cumplimiento de metas
        st.subheader("🎯 Proyección de Metas Financieras")
        
        if planner.planned_purchases:
            projection_data = []
            cumulative_saved = 0
            
            for i in range(12):  # Próximos 12 meses
                future_date = datetime.now() + timedelta(days=30 * i)
                month_savings = sum(p['monthly_save'] for p in planner.planned_purchases if p['amount_saved'] < p['price'])
                cumulative_saved += month_savings
                
                completed_goals = sum(1 for p in planner.planned_purchases 
                                    if p['amount_saved'] + (month_savings * i) >= p['price'])
                
                projection_data.append({
                    'Mes': future_date.strftime('%Y-%m'),
                    'Ahorro Acumulado': cumulative_saved,
                    'Metas Completadas': completed_goals
                })
            
            proj_df = pd.DataFrame(projection_data)
            
            fig_projection = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig_projection.add_trace(
                go.Scatter(x=proj_df['Mes'], y=proj_df['Ahorro Acumulado'], 
                          name='Ahorro Acumulado', line=dict(color='#00b894')),
                secondary_y=False,
            )
            
            fig_projection.add_trace(
                go.Scatter(x=proj_df['Mes'], y=proj_df['Metas Completadas'], 
                          name='Metas Completadas', line=dict(color='#667eea')),
                secondary_y=True,
            )
            
            fig_projection.update_xaxes(title_text="Mes")
            fig_projection.update_yaxes(title_text="Monto Ahorrado (COP)", secondary_y=False)
            fig_projection.update_yaxes(title_text="Número de Metas", secondary_y=True)
            fig_projection.update_layout(title_text="Proyección de Cumplimiento de Metas")
            
            st.plotly_chart(fig_projection, use_container_width=True)
    
    with tab6:
        st.header("⚙️ Configuración y Herramientas")
        
        # Exportar reportes
        st.subheader("📊 Reportes y Exportación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Exportar Reporte Mensual"):
                current_month = datetime.now().month
                current_year = datetime.now().year
                
                # Generar reporte
                report_data = {
                    'mes': calendar.month_name[current_month],
                    'año': current_year,
                    'salario': planner.income,
                    'presupuesto': planner.calculate_percentages(),
                    'gastos_reales': planner.expense_tracker.get_category_totals(
                        datetime(current_year, current_month, 1).date(),
                        datetime.now().date()
                    ),
                    'compras_planificadas': len(planner.planned_purchases),
                    'nivel_riesgo': planner.get_risk_analysis()['level']
                }
                
                # Crear CSV de gastos
                if planner.expense_tracker.daily_expenses:
                    expenses_df = pd.DataFrame(planner.expense_tracker.daily_expenses)
                    csv_data = expenses_df.to_csv(index=False)
                    
                    st.download_button(
                        label="⬇️ Descargar Gastos (CSV)",
                        data=csv_data,
                        file_name=f"gastos_{current_year}_{current_month:02d}.csv",
                        mime="text/csv"
                    )
        
        with col2:
            if st.button("🔄 Reiniciar Datos"):
                if st.button("⚠️ Confirmar Reinicio", key="confirm_reset"):
                    st.session_state.planner = FinancialPlanner()
                    st.success("✅ Datos reiniciados")
                    st.rerun()
        
        # Configuraciones avanzadas
        st.subheader("🔧 Configuraciones Avanzadas")
        
        with st.expander("📱 Notificaciones y Alertas"):
            enable_alerts = st.checkbox("Activar alertas de presupuesto", value=True)
            alert_threshold = st.slider("Alerta cuando gaste el % del presupuesto", 80, 100, 90)
            
            daily_expense_limit = st.number_input(
                "Límite diario de gastos impulsivos (COP)",
                min_value=0,
                value=50000,
                step=10000
            )
        
        with st.expander("🎯 Personalización de Categorías"):
            st.write("**Agregar subcategorías personalizadas:**")
            
            new_category = st.selectbox("Categoría principal", ["Necesidades", "Deseos", "Ahorros"])
            new_subcategory = st.text_input("Nueva subcategoría", placeholder="Ej: Gimnasio, Masajes, etc.")
            
            if st.button("➕ Agregar Subcategoría"):
                if new_subcategory:
                    # Esta funcionalidad se puede expandir para personalizar categorías
                    st.success(f"✅ Subcategoría '{new_subcategory}' agregada a {new_category}")
        
        # Estadísticas generales
        st.subheader("📈 Estadísticas Generales")
        
        if planner.expense_tracker.daily_expenses:
            total_expenses = sum(e['amount'] for e in planner.expense_tracker.daily_expenses)
            total_transactions = len(planner.expense_tracker.daily_expenses)
            avg_transaction = total_expenses / total_transactions if total_transactions > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("💳 Total Gastado", f"${total_expenses:,.0f}")
            
            with col2:
                st.metric("📊 Transacciones", total_transactions)
            
            with col3:
                st.metric("📱 Gasto Promedio", f"${avg_transaction:,.0f}")
            
            # Gráfico de gastos por día de la semana
            expense_df = pd.DataFrame(planner.expense_tracker.daily_expenses)
            expense_df['day_of_week'] = pd.to_datetime(expense_df['date']).dt.day_name()
            
            daily_spending = expense_df.groupby('day_of_week')['amount'].sum().reset_index()
            
            fig_daily = px.bar(
                daily_spending,
                x='day_of_week',
                y='amount',
                title="Gastos por Día de la Semana",
                color='amount',
                color_continuous_scale='Blues'
            )
            
            st.plotly_chart(fig_daily, use_container_width=True)
        
        # Herramientas adicionales
        st.subheader("🛠️ Herramientas Financieras")
        
        with st.expander("🧮 Calculadora de Interés Compuesto"):
            initial_amount = st.number_input("Monto inicial", min_value=0, value=100000, step=50000)
            monthly_contribution = st.number_input("Aporte mensual", min_value=0, value=50000, step=10000)
            annual_rate = st.number_input("Tasa anual (%)", min_value=0.0, value=8.0, step=0.5) / 100
            years = st.number_input("Años", min_value=1, value=10, step=1)
            
            if st.button("📊 Calcular"):
                months = years * 12
                monthly_rate = annual_rate / 12
                
                # Cálculo de interés compuesto con aportes mensuales
                future_value = initial_amount * (1 + monthly_rate)**months
                
                if monthly_rate > 0:
                    annuity_value = monthly_contribution * (((1 + monthly_rate)**months - 1) / monthly_rate)
                else:
                    annuity_value = monthly_contribution * months
                
                total_future_value = future_value + annuity_value
                total_contributed = initial_amount + (monthly_contribution * months)
                total_interest = total_future_value - total_contributed
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("💰 Valor Final", f"${total_future_value:,.0f}")
                
                with col2:
                    st.metric("💵 Total Aportado", f"${total_contributed:,.0f}")
                
                with col3:
                    st.metric("📈 Intereses Ganados", f"${total_interest:,.0f}")
        
        with st.expander("💳 Calculadora de Deudas"):
            debt_amount = st.number_input("Monto de la deuda", min_value=0, value=1000000, step=100000)
            debt_rate = st.number_input("Tasa mensual (%)", min_value=0.0, value=2.5, step=0.1) / 100
            monthly_payment = st.number_input("Pago mensual", min_value=0, value=100000, step=10000)
            
            if st.button("🔍 Analizar Deuda") and debt_amount > 0 and monthly_payment > 0:
                if monthly_payment <= debt_amount * debt_rate:
                    st.error("⚠️ El pago mensual no cubre ni los intereses. Aumente el pago.")
                else:
                    # Calcular tiempo de pago
                    if debt_rate > 0:
                        months_to_pay = math.ceil(
                            -math.log(1 - (debt_amount * debt_rate / monthly_payment)) / math.log(1 + debt_rate)
                        )
                    else:
                        months_to_pay = math.ceil(debt_amount / monthly_payment)
                    
                    total_paid = monthly_payment * months_to_pay
                    total_interest = total_paid - debt_amount
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("⏰ Meses para pagar", months_to_pay)
                    
                    with col2:
                        st.metric("💰 Total a pagar", f"${total_paid:,.0f}")
                    
                    with col3:
                        st.metric("💸 Intereses totales", f"${total_interest:,.0f}")

if __name__ == "__main__":
    main()
