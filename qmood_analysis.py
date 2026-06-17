"""
QMOOD Tabanlı Yazılım Kalitesi Analizi
OpenSearch Anomaly Detection Projesi

Bansiya & Davis (2002) formüllerine dayalı QMOOD hesaplamaları.
CK Tool çıktılarından tasarım özellikleri ve kalite nitelikleri hesaplanır.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import json

VERSIONS = ["1.0.0.0", "1.1.0.0", "1.3.0.0", "2.0.0.0", "2.2.0.0",
            "2.4.0.0", "2.7.0.0", "2.10.0.0", "2.13.0.0", "2.16.0.0",
            "2.19.0.0", "3.0.0.0"]

METRICS_DIR = "/Users/bilgem/software_design_project/metrics"
OUTPUT_DIR = "/Users/bilgem/software_design_project/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_version_data(version):
    """Bir sürümün CK Tool çıktısını yükler."""
    path = os.path.join(METRICS_DIR, version, "class.csv")
    df = pd.read_csv(path)
    # Sadece somut sınıfları al (inner class ve anonymous hariç tutulabilir ama dahil edelim)
    return df


def compute_design_properties(df):
    """
    CK Tool metriklerinden QMOOD tasarım özelliklerini hesaplar.

    Tasarım Özellikleri ve Eşlemeler (Bansiya & Davis, 2002):
    - Design Size (DSC): Toplam sınıf sayısı
    - Abstraction (ANA): Ortalama soyut sınıf oranı (abstract methods / total methods)
    - Encapsulation (DAM): Data Access Metric = private fields / total fields oranı
    - Coupling (DCC): Direct Class Coupling = ortalama CBO
    - Cohesion (CAM): Cohesion Among Methods = 1 - ortalama LCOM* (normalize)
    - Composition (MOA): Measure of Aggregation = ortalama NOA (field sayısı)
    - Inheritance (MFA): Measure of Functional Abstraction = DIT tabanlı
    - Polymorphism (NOP): Number of Polymorphic methods
    - Messaging (CIS): Class Interface Size = ortalama public method sayısı
    - Complexity (NOM): Number of Methods = ortalama metot sayısı
    """
    n_classes = len(df)

    # DSC - Design Size: toplam sınıf sayısı
    dsc = n_classes

    # ANA - Abstraction: ortalama abstract method oranı
    total_methods = df['totalMethodsQty'].replace(0, 1)
    ana = (df['abstractMethodsQty'] / total_methods).mean()

    # DAM - Data Access Metric (Encapsulation): private fields / total fields
    total_fields = df['totalFieldsQty'].replace(0, 1)
    dam = (df['privateFieldsQty'] / total_fields).mean()

    # DCC - Direct Class Coupling: ortalama CBO
    dcc = df['cbo'].mean()

    # CAM - Cohesion Among Methods: TCC (Tight Class Cohesion) kullanılır
    # CK Tool tcc verir, NaN olanları 0 olarak al
    tcc_values = pd.to_numeric(df['tcc'], errors='coerce').fillna(0)
    cam = tcc_values.mean()

    # MOA - Measure of Aggregation: ortalama alan sayısı (non-primitive yaklaşımı)
    # CK Tool doğrudan MOA vermez, totalFieldsQty - staticFieldsQty kullanılır
    moa = (df['totalFieldsQty'] - df['staticFieldsQty']).mean()

    # MFA - Measure of Functional Abstraction: inherited methods oranı
    # DIT > 0 olan sınıfların oranı (inheritance kullanımı)
    mfa = (df['dit'] > 0).mean()

    # NOP - Number of Polymorphic methods: abstractMethodsQty + overriding yaklaşımı
    nop = df['abstractMethodsQty'].mean() + (df['dit'] > 0).mean()

    # CIS - Class Interface Size: ortalama public method sayısı
    cis = df['publicMethodsQty'].mean()

    # NOM - Number of Methods (Complexity): ortalama WMC
    nom = df['wmc'].mean()

    return {
        'DSC': dsc,
        'ANA': ana,
        'DAM': dam,
        'DCC': dcc,
        'CAM': cam,
        'MOA': moa,
        'MFA': mfa,
        'NOP': nop,
        'CIS': cis,
        'NOM': nom
    }


def compute_quality_attributes(dp):
    """
    QMOOD kalite niteliklerini Bansiya & Davis (2002) formülleriyle hesaplar.

    Formüller:
    Reusability     = -0.25*DCC + 0.25*CAM + 0.5*CIS + 0.5*DSC
    Flexibility     = 0.25*DAM - 0.25*DCC + 0.5*MOA + 0.5*NOP
    Understandability = -0.33*ANA + 0.33*DAM - 0.33*DCC + 0.33*CAM - 0.33*NOP - 0.33*NOM - 0.33*DSC
    Functionality   = 0.12*CAM + 0.22*NOP + 0.22*CIS + 0.22*DSC + 0.22*ANA
    Extendibility   = 0.5*ANA - 0.5*DCC + 0.5*MFA + 0.5*NOP
    Effectiveness   = 0.2*ANA + 0.2*DAM + 0.2*MOA + 0.2*MFA + 0.2*NOP
    """
    # Normalizasyon: DSC büyük değer olduğundan normalize edelim
    # QMOOD'da metrikler genellikle normalize edilir
    # DSC'yi log scale ile normalize ediyoruz
    dsc_norm = np.log2(dp['DSC'] + 1)

    reusability = (-0.25 * dp['DCC'] + 0.25 * dp['CAM'] +
                   0.5 * dp['CIS'] + 0.5 * dsc_norm)

    flexibility = (0.25 * dp['DAM'] - 0.25 * dp['DCC'] +
                   0.5 * dp['MOA'] + 0.5 * dp['NOP'])

    understandability = (-0.33 * dp['ANA'] + 0.33 * dp['DAM'] -
                         0.33 * dp['DCC'] + 0.33 * dp['CAM'] -
                         0.33 * dp['NOP'] - 0.33 * dp['NOM'] -
                         0.33 * dsc_norm)

    functionality = (0.12 * dp['CAM'] + 0.22 * dp['NOP'] +
                     0.22 * dp['CIS'] + 0.22 * dsc_norm +
                     0.22 * dp['ANA'])

    extendibility = (0.5 * dp['ANA'] - 0.5 * dp['DCC'] +
                     0.5 * dp['MFA'] + 0.5 * dp['NOP'])

    effectiveness = (0.2 * dp['ANA'] + 0.2 * dp['DAM'] +
                     0.2 * dp['MOA'] + 0.2 * dp['MFA'] +
                     0.2 * dp['NOP'])

    return {
        'Reusability': reusability,
        'Flexibility': flexibility,
        'Understandability': understandability,
        'Functionality': functionality,
        'Extendibility': extendibility,
        'Effectiveness': effectiveness
    }


def compute_raw_metrics_summary(df):
    """Her sürüm için ham metriklerin özetini hesaplar."""
    return {
        'Total_Classes': len(df),
        'Avg_CBO': df['cbo'].mean(),
        'Avg_DIT': df['dit'].mean(),
        'Avg_WMC': df['wmc'].mean(),
        'Avg_RFC': df['rfc'].mean(),
        'Avg_LCOM': df['lcom'].mean(),
        'Avg_NOM': df['totalMethodsQty'].mean(),
        'Avg_NOA': df['totalFieldsQty'].mean(),
        'Avg_LOC': df['loc'].mean(),
        'Total_LOC': df['loc'].sum(),
        'Avg_NOC': df['noc'].mean(),
        'Max_CBO': df['cbo'].max(),
        'Max_WMC': df['wmc'].max(),
        'Max_DIT': df['dit'].max(),
    }


# ============================================================
# ANA ANALİZ
# ============================================================
print("=" * 60)
print("QMOOD ANALİZİ - OpenSearch Anomaly Detection")
print("=" * 60)

all_design_props = {}
all_quality_attrs = {}
all_raw_metrics = {}

for version in VERSIONS:
    print(f"\nSürüm: {version}")
    df = load_version_data(version)

    dp = compute_design_properties(df)
    qa = compute_quality_attributes(dp)
    raw = compute_raw_metrics_summary(df)

    all_design_props[version] = dp
    all_quality_attrs[version] = qa
    all_raw_metrics[version] = raw

    print(f"  Sınıf sayısı: {len(df)}")
    print(f"  Reusability: {qa['Reusability']:.4f}")
    print(f"  Flexibility: {qa['Flexibility']:.4f}")
    print(f"  Understandability: {qa['Understandability']:.4f}")
    print(f"  Functionality: {qa['Functionality']:.4f}")
    print(f"  Extendibility: {qa['Extendibility']:.4f}")
    print(f"  Effectiveness: {qa['Effectiveness']:.4f}")

# DataFrame'lere dönüştür
dp_df = pd.DataFrame(all_design_props).T
dp_df.index.name = 'Version'

qa_df = pd.DataFrame(all_quality_attrs).T
qa_df.index.name = 'Version'

raw_df = pd.DataFrame(all_raw_metrics).T
raw_df.index.name = 'Version'

# CSV olarak kaydet
dp_df.to_csv(os.path.join(OUTPUT_DIR, 'design_properties.csv'))
qa_df.to_csv(os.path.join(OUTPUT_DIR, 'quality_attributes.csv'))
raw_df.to_csv(os.path.join(OUTPUT_DIR, 'raw_metrics.csv'))

print("\n\n" + "=" * 60)
print("TASARIM ÖZELLİKLERİ TABLOSU")
print("=" * 60)
print(dp_df.round(4).to_string())

print("\n\n" + "=" * 60)
print("KALİTE NİTELİKLERİ TABLOSU")
print("=" * 60)
print(qa_df.round(4).to_string())

print("\n\n" + "=" * 60)
print("HAM METRİKLER TABLOSU")
print("=" * 60)
print(raw_df.round(4).to_string())

# ============================================================
# GÖRSELLEŞTİRME
# ============================================================
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11

short_versions = [v.replace('.0.0', '.0').replace('.0', '') if v.count('.') > 1 else v for v in VERSIONS]
# Daha kısa etiketler
short_labels = ['v' + v for v in VERSIONS]

# 1. Kalite Nitelikleri Zaman Serisi
fig, ax = plt.subplots(figsize=(14, 8))
colors = ['#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0', '#00BCD4']
markers = ['o', 's', '^', 'D', 'v', 'p']

for i, attr in enumerate(qa_df.columns):
    ax.plot(range(len(VERSIONS)), qa_df[attr], marker=markers[i], linewidth=2.5,
            markersize=8, label=attr, color=colors[i])

ax.set_xticks(range(len(VERSIONS)))
ax.set_xticklabels(short_labels, rotation=45, ha='right')
ax.set_xlabel('Sürüm', fontsize=13)
ax.set_ylabel('QMOOD Skoru', fontsize=13)
ax.set_title('OpenSearch Anomaly Detection — QMOOD Kalite Nitelikleri Evrimi', fontsize=15, fontweight='bold')
ax.legend(loc='best', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'quality_attributes_evolution.png'), dpi=150)
plt.close()

# 2. Tasarım Özellikleri Zaman Serisi (seçili olanlar)
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
design_props_to_plot = ['DSC', 'DCC', 'CAM', 'DAM', 'NOM', 'CIS']
dp_colors = ['#1976D2', '#D32F2F', '#388E3C', '#7B1FA2', '#F57C00', '#0097A7']

for idx, (prop, color) in enumerate(zip(design_props_to_plot, dp_colors)):
    ax = axes[idx // 3][idx % 3]
    ax.plot(range(len(VERSIONS)), dp_df[prop], marker='o', linewidth=2.5,
            markersize=7, color=color)
    ax.fill_between(range(len(VERSIONS)), dp_df[prop], alpha=0.15, color=color)
    ax.set_xticks(range(len(VERSIONS)))
    ax.set_xticklabels(short_labels, rotation=45, ha='right', fontsize=9)
    ax.set_title(prop, fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)

plt.suptitle('OpenSearch Anomaly Detection — Tasarım Özellikleri Evrimi', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'design_properties_evolution.png'), dpi=150)
plt.close()

# 3. Ham Metrikler - Büyüme Grafiği
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Sınıf sayısı ve LOC
axes[0][0].plot(range(len(VERSIONS)), raw_df['Total_Classes'], 'o-', linewidth=2.5, color='#1565C0', markersize=7)
axes[0][0].fill_between(range(len(VERSIONS)), raw_df['Total_Classes'], alpha=0.15, color='#1565C0')
axes[0][0].set_title('Toplam Sınıf Sayısı', fontsize=13, fontweight='bold')
axes[0][0].set_xticks(range(len(VERSIONS)))
axes[0][0].set_xticklabels(short_labels, rotation=45, ha='right', fontsize=9)

axes[0][1].plot(range(len(VERSIONS)), raw_df['Total_LOC'], 'o-', linewidth=2.5, color='#C62828', markersize=7)
axes[0][1].fill_between(range(len(VERSIONS)), raw_df['Total_LOC'], alpha=0.15, color='#C62828')
axes[0][1].set_title('Toplam LOC (Kod Satırı)', fontsize=13, fontweight='bold')
axes[0][1].set_xticks(range(len(VERSIONS)))
axes[0][1].set_xticklabels(short_labels, rotation=45, ha='right', fontsize=9)

# Avg CBO ve Avg WMC
axes[1][0].plot(range(len(VERSIONS)), raw_df['Avg_CBO'], 'o-', linewidth=2.5, color='#E65100', markersize=7)
axes[1][0].fill_between(range(len(VERSIONS)), raw_df['Avg_CBO'], alpha=0.15, color='#E65100')
axes[1][0].set_title('Ortalama CBO (Coupling)', fontsize=13, fontweight='bold')
axes[1][0].set_xticks(range(len(VERSIONS)))
axes[1][0].set_xticklabels(short_labels, rotation=45, ha='right', fontsize=9)

axes[1][1].plot(range(len(VERSIONS)), raw_df['Avg_WMC'], 'o-', linewidth=2.5, color='#4A148C', markersize=7)
axes[1][1].fill_between(range(len(VERSIONS)), raw_df['Avg_WMC'], alpha=0.15, color='#4A148C')
axes[1][1].set_title('Ortalama WMC (Complexity)', fontsize=13, fontweight='bold')
axes[1][1].set_xticks(range(len(VERSIONS)))
axes[1][1].set_xticklabels(short_labels, rotation=45, ha='right', fontsize=9)

for ax in axes.flat:
    ax.grid(True, alpha=0.3)

plt.suptitle('OpenSearch Anomaly Detection — Ham Metrik Evrimi', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'raw_metrics_evolution.png'), dpi=150)
plt.close()

# 4. Heatmap - Kalite Nitelikleri Delta (Sürümler Arası Fark)
qa_delta = qa_df.diff()
qa_delta = qa_delta.iloc[1:]  # İlk satır NaN

fig, ax = plt.subplots(figsize=(12, 6))
im = ax.imshow(qa_delta.T.values, cmap='RdYlGn', aspect='auto')
ax.set_xticks(range(len(qa_delta)))
ax.set_xticklabels([f'{VERSIONS[i]}→{VERSIONS[i+1]}' for i in range(len(VERSIONS)-1)],
                   rotation=45, ha='right', fontsize=9)
ax.set_yticks(range(len(qa_delta.columns)))
ax.set_yticklabels(qa_delta.columns, fontsize=11)
ax.set_title('Sürümler Arası Kalite Değişimi (Delta)', fontsize=14, fontweight='bold')

# Değerleri hücrelere yaz
for i in range(len(qa_delta.columns)):
    for j in range(len(qa_delta)):
        val = qa_delta.T.values[i, j]
        color = 'white' if abs(val) > (qa_delta.T.values.max() - qa_delta.T.values.min()) * 0.4 else 'black'
        ax.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=8, color=color)

plt.colorbar(im, label='Değişim Miktarı')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'quality_delta_heatmap.png'), dpi=150)
plt.close()

# 5. Radar Chart - İlk vs Son Sürüm Karşılaştırma
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
categories = list(qa_df.columns)
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# Normalize (0-1 arası)
qa_min = qa_df.min()
qa_max = qa_df.max()
qa_range = qa_max - qa_min
qa_range = qa_range.replace(0, 1)
qa_norm = (qa_df - qa_min) / qa_range

first_vals = qa_norm.iloc[0].values.tolist() + [qa_norm.iloc[0].values[0]]
last_vals = qa_norm.iloc[-1].values.tolist() + [qa_norm.iloc[-1].values[0]]
mid_vals = qa_norm.iloc[len(VERSIONS)//2].values.tolist() + [qa_norm.iloc[len(VERSIONS)//2].values[0]]

ax.plot(angles, first_vals, 'o-', linewidth=2, color='#2196F3', label=f'v{VERSIONS[0]}')
ax.fill(angles, first_vals, alpha=0.1, color='#2196F3')
ax.plot(angles, mid_vals, 's-', linewidth=2, color='#FF9800', label=f'v{VERSIONS[len(VERSIONS)//2]}')
ax.fill(angles, mid_vals, alpha=0.1, color='#FF9800')
ax.plot(angles, last_vals, '^-', linewidth=2, color='#F44336', label=f'v{VERSIONS[-1]}')
ax.fill(angles, last_vals, alpha=0.1, color='#F44336')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11)
ax.set_title('Kalite Nitelikleri Radar Karşılaştırması\n(Normalize Edilmiş)', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'quality_radar_comparison.png'), dpi=150)
plt.close()

# 6. Coupling vs Cohesion (Mimari Bozulma Göstergesi)
fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(dp_df['DCC'], dp_df['CAM'],
                     s=[raw_df.loc[v, 'Total_Classes']/2 for v in VERSIONS],
                     c=range(len(VERSIONS)), cmap='coolwarm', alpha=0.8, edgecolors='black', linewidth=1)

for i, v in enumerate(VERSIONS):
    ax.annotate(f'v{v}', (dp_df.loc[v, 'DCC'], dp_df.loc[v, 'CAM']),
                textcoords="offset points", xytext=(8, 5), fontsize=9)

ax.set_xlabel('DCC (Coupling)', fontsize=13)
ax.set_ylabel('CAM (Cohesion)', fontsize=13)
ax.set_title('Coupling vs Cohesion — Mimari Bozulma Analizi\n(Daire boyutu = sınıf sayısı)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.colorbar(scatter, label='Sürüm Sırası (eski → yeni)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'coupling_vs_cohesion.png'), dpi=150)
plt.close()

# Delta tablosunu kaydet
qa_delta.to_csv(os.path.join(OUTPUT_DIR, 'quality_delta.csv'))

print("\n\n" + "=" * 60)
print("TÜM GRAFİKLER VE TABLOLAR OLUŞTURULDU")
print("=" * 60)
print(f"Çıktı dizini: {OUTPUT_DIR}")
print("Dosyalar:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    print(f"  - {f}")

# JSON olarak da kaydet (LLM promptları için)
analysis_data = {
    'project': 'OpenSearch Anomaly Detection',
    'versions': VERSIONS,
    'design_properties': {v: {k: round(val, 4) for k, val in dp.items()}
                          for v, dp in all_design_props.items()},
    'quality_attributes': {v: {k: round(val, 4) for k, val in qa.items()}
                           for v, qa in all_quality_attrs.items()},
    'raw_metrics': {v: {k: round(float(val), 2) for k, val in rm.items()}
                    for v, rm in all_raw_metrics.items()}
}

with open(os.path.join(OUTPUT_DIR, 'analysis_data.json'), 'w') as f:
    json.dump(analysis_data, f, indent=2)

print("\nanalysis_data.json oluşturuldu (LLM promptları için)")
