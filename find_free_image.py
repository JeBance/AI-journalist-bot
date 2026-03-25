#!/usr/bin/env python3
"""
Поиск свободных изображений для статей.

Источники:
- Unsplash (бесплатно, без авторских прав)
- Pexels (бесплатно, без авторских прав)
- Pixabay (бесплатно, без авторских прав)
"""

import requests
import random

def get_unsplash_image_url(query, width=1200, height=630):
    """
    Получить случайное изображение с Unsplash по запросу.
    
    Unsplash API не требует ключа для простого поиска через source API.
    Все изображения бесплатны для коммерческого и некоммерческого использования.
    
    Args:
        query: Поисковый запрос (например, "artificial intelligence")
        width: Ширина изображения
        height: Высота изображения
    
    Returns:
        str: URL изображения
    """
    # Unsplash Source API (не требует ключа)
    url = f"https://source.unsplash.com/{width}x{height}/?{query}"
    
    # Делаем запрос (получаем редирект на реальное изображение)
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except:
        # Фолбэк на прямой URL
        return f"https://images.unsplash.com/photo-1677442136019-21780ecad995?w={width}&h={height}&fit=crop"

def get_pexels_image_url(query, api_key=None):
    """
    Получить изображение с Pexels.
    
    Требуется API ключ (бесплатно): https://www.pexels.com/api/
    """
    if not api_key:
        # Возвращаем placeholder
        return None
    
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": 1}
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    
    if result.get("photos"):
        return result["photos"][0]["src"]["landscape"]
    
    return None

def get_image_for_article(topic):
    """
    Получить URL изображения для темы статьи.
    
    Используем прямые URL с Pexels/Pixabay (бесплатно, без авторских прав).
    
    Args:
        topic: Тема статьи (например, "AI journalism", "programming")
    
    Returns:
        str: URL изображения или None
    """
    # Словарь тем → прямые URL изображений
    # Все изображения с Pexels/Pixabay — бесплатные, без авторских прав
    
    topic_images = {
        "ai": "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "artificial intelligence": "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "journalism": "https://images.pexels.com/photos/159711/books-book-pages-book-literature-159711.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "technology": "https://images.pexels.com/photos/196644/pexels-photo-196644.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "programming": "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "code": "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "python": "https://images.pexels.com/photos/577585/pexels-photo-577585.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "javascript": "https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "vpn": "https://images.pexels.com/photos/5380642/pexels-photo-5380642.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "security": "https://images.pexels.com/photos/60504/security-protection-anti-virus-software-60504.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "hardware": "https://images.pexels.com/photos/916293/pexels-photo-916293.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "css": "https://images.pexels.com/photos/577585/pexels-photo-577585.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "php": "https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "databases": "https://images.pexels.com/photos/60504/security-protection-anti-virus-software-60504.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "devops": "https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "cloud": "https://images.pexels.com/photos/258244/pexels-photo-258244.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "neural network": "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "machine learning": "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg?auto=compress&cs=tinysrgb&w=1200",
    }
    
    # Ищем подходящее изображение
    topic_lower = topic.lower()
    
    for key, url in topic_images.items():
        if key in topic_lower:
            return url
    
    # Фолбэк — изображение по умолчанию (технологии)
    return "https://images.pexels.com/photos/196644/pexels-photo-196644.jpeg?auto=compress&cs=tinysrgb&w=1200"

def test_image_search():
    """Тестирование поиска изображений."""
    topics = [
        "artificial intelligence",
        "programming",
        "journalism",
        "cybersecurity"
    ]
    
    print("🔍 Поиск изображений...")
    print()
    
    for topic in topics:
        url = get_image_for_article(topic)
        print(f"📷 {topic}:")
        print(f"   {url}")
        print()

if __name__ == "__main__":
    test_image_search()
