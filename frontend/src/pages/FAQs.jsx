import React from 'react';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../components/ui/accordion';

const FAQs = () => {
  const faqs = [
    {
      question: 'Is Fobi really free?',
      answer: 'Yes! Fobi is 100% free to use. You can create unlimited chatbots from your Google Forms without any cost or hidden fees.'
    },
    {
      question: 'Do I need to register to use Fobi?',
      answer: 'No registration required! Simply paste your Google Form link, customize your chatbot, and embed it on your website. It\'s that simple.'
    },
    {
      question: 'What happens to the data collected through the chatbot?',
      answer: 'All responses are sent directly to your Google Form, just like they would be if someone filled out the form directly. Fobi doesn\'t store or access any of your data.'
    },
    {
      question: 'Can I customize the appearance of my chatbot?',
      answer: 'Absolutely! You can customize colors, size, text, and positioning to match your brand perfectly. The chatbot is fully customizable to fit your website\'s design.'
    },
    {
      question: 'How do I embed the chatbot on my website?',
      answer: 'Fobi provides two embedding options: a Chat PopUp widget that appears in the corner of your page, or an IFrame that you can embed directly into your page content. Both options come with simple copy-paste code.'
    },
    {
      question: 'Will the chatbot work on mobile devices?',
      answer: 'Yes! Fobi chatbots are fully responsive and work seamlessly on all devices - desktop, tablet, and mobile phones.'
    },
    {
      question: 'Can I use Fobi with any Google Form?',
      answer: 'Yes! Fobi works with any publicly accessible Google Form. Just make sure your form settings allow responses from anyone.'
    },
    {
      question: 'How long does it take to set up a chatbot?',
      answer: 'You can create and embed your first chatbot in less than 5 minutes! The process is incredibly simple - paste your form link, customize, and embed.'
    },
    {
      question: 'What are the benefits of using a chatbot instead of a regular form?',
      answer: 'Chatbots provide a more engaging and conversational experience, leading to higher completion rates (up to 90% improvement). They feel more personal, reduce friction, and make data collection more enjoyable for your users.'
    },
    {
      question: 'Can I edit my chatbot after embedding it?',
      answer: 'Yes! You can edit your Google Form at any time, and the changes will automatically reflect in your chatbot. For design changes, you can regenerate the embed code with new customizations.'
    },
    {
      question: 'Is there a limit to how many responses I can collect?',
      answer: 'The response limit is determined by your Google Form settings. Fobi itself doesn\'t impose any limits on the number of responses you can collect.'
    },
    {
      question: 'What browsers are supported?',
      answer: 'Fobi works on all modern browsers including Chrome, Firefox, Safari, and Edge. It\'s built with modern web standards to ensure broad compatibility.'
    }
  ];

  return (
    <div className="min-h-screen bg-white pt-24 pb-16">
      <div className="container mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Frequently Asked Questions
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Everything you need to know about Fobi. Can't find the answer you're looking for? Feel free to reach out to us at info@fobi.io
          </p>
        </div>

        {/* FAQ Accordion */}
        <div className="max-w-4xl mx-auto">
          <Accordion type="single" collapsible className="w-full space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem 
                key={index} 
                value={`item-${index}`}
                className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl px-6 border border-purple-100 shadow-sm hover:shadow-md transition-all"
              >
                <AccordionTrigger className="text-left text-lg font-semibold text-gray-900 hover:text-purple-600 py-6">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-gray-700 pb-6 leading-relaxed">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>

        {/* Contact CTA */}
        <div className="mt-20 text-center">
          <div className="bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-600 rounded-2xl p-12 shadow-xl text-white">
            <h2 className="text-3xl font-bold mb-4">Still have questions?</h2>
            <p className="text-white/90 mb-8 max-w-2xl mx-auto text-lg">
              We're here to help! Reach out to our team and we'll get back to you as soon as possible.
            </p>
            <a 
              href="mailto:info@fobi.io"
              className="inline-block bg-white text-purple-600 px-8 py-4 rounded-full font-semibold text-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
            >
              Contact Us
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FAQs;